import tensorflow as tf
import numpy as np
import os, argparse, time, random

from chat_module.ner.model import SpecModel
from chat_module.ner.utils import get_sentence, get_transform, preprocess_data, BatchManager, load_wordvec
from chat_module.ner.conlleval import return_report

from chat_module.ner.tools import cn_to_zh, zh_to_cn, load_input_sentence

def ner_sent(text):
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
    config.gpu_options.allow_growth = True # allocate dynamically

    ## hyperparameters
    args = {}
    args['embedding_size'] = 100
    args['hidden_size'] = 150
    args['dropout'] = 0.5
    args['PROJ'] = 'Linear'
    args['lr'] = 0.001
    args['grad_clip'] = 5.0
    args['project_size'] = 150
    args['batch_size'] = 20
    args['mode'] = 'demo'
    args['epochs'] = 40
    args['model_path'] = 'ckpt'
    args['demo_model_path'] = '20200121'

    import pickle
    with open('./chat_module/ner/maps.pkl', 'rb') as fr:
        info = pickle.load(fr)
        char2id = info[0]
        id2char = info[1]
        transfer_tag2id = info[4]
        transfer_id2tag = info[5]

    ### find the latest demo model
    demo_path = os.path.join("./chat_module/ner/", args['demo_model_path']) + "/"
    ckpt_file = tf.train.latest_checkpoint(demo_path)

    model = SpecModel(args=args,
                      num_tags=len(transfer_id2tag),
                      vocab_size=len(id2char),
                      name='transfer')
    model.build()
    saver = tf.train.Saver()

    with tf.Session(config=config) as sess:
        saver.restore(sess, ckpt_file)

        demo_sent = text.strip()
        demo_sent = demo_sent.replace(" ", "")
        demo_sent = zh_to_cn(demo_sent)

        demo_transfer_test = load_input_sentence(demo_sent)
        demo_transfer_test_data = preprocess_data(demo_transfer_test, char2id, transfer_tag2id)
        demo_transfer_test_manager = BatchManager(demo_transfer_test_data, args['batch_size'])
        demo_data = model.evaluate(sess, demo_transfer_test_manager, transfer_id2tag)

        ret = {
                "product_name": [], "time": [], "person_name": [], "org_name": [],
                "company_name": [], "location": [], "event": [],
              }

        isWord = False
        tempWord = ""
        tempTag = ""
        lastIdx = len(demo_data[0]) - 1
        idx = 0
        for sect in demo_data[0]:
            char, _, tag = sect.split(" ")

            if (tag == "O" or "B-" in tag) and isWord:
                ret[tempTag].append(cn_to_zh(tempWord))
                isWord = False
                tempTag = ""
                tempWord = ""

            if tag != "O":
                if not isWord:
                    tempTag = tag[2:]
                    isWord = True
                tempWord += char

            if idx == lastIdx and tag != "O":
                ret[tempTag].append(cn_to_zh(tempWord))

            idx += 1

    return ret

def ques_and_ans(ent_q, ent_a):
    ret = {
            "product_name": [], "time": [], "person_name": [], "org_name": [],
            "company_name": [], "location": [], "event": [],
          }

    for key in ret:
        ret[key] = (ent_q[key] + ent_a[key])

    return ret
