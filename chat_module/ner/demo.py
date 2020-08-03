import numpy as np
import os, argparse, time, random

from chat_module.ner.model import SpecModel
from chat_module.ner.utils import get_sentence, get_transform, preprocess_data, BatchManager, load_wordvec
from chat_module.ner.conlleval import return_report

from chat_module.ner.tools import cn_to_zh, zh_to_cn, load_input_sentence
from flask_restful import reqparse

def ner_sent(text):
    import tensorflow as tf
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
    config.gpu_options.allow_growth = True # allocate dynamically

    ## hyperparameters
    # parser = argparse.ArgumentParser(description='Transfer Learning on BiLSTM-CRF for Chinese NER task')
    parser = reqparse.RequestParser()
    parser.add_argument('embedding_size', type=int, default=100, help='char embedding_dim')
    parser.add_argument('hidden_size', type=int, default=150, help='dim of lstm hidden state')
    parser.add_argument('dropout', type=float, default=0.5, help='dropout keep_prob')
    parser.add_argument('PROJ', type=str, default='Linear', help='use domain masks or not')
    parser.add_argument('lr', type=float, default=0.001, help='learning rate')
    parser.add_argument('grad_clip', type=float, default=5.0, help='gradient clipping')
    parser.add_argument('project_size', type=int, default=150, help='dim of project hidden state')
    parser.add_argument('batch_size', type=int, default=20, help='#sample of each minibatch')
    parser.add_argument('mode', type=str, default='demo', help='mode of want')
    parser.add_argument('epochs', type=int, default=40, help='nums of epochs')
    parser.add_argument('train_data', type=str, default='data/train', help='normal train data')
    parser.add_argument('test_data', type=str, default='data/test', help='normal test data')
    parser.add_argument('transfer_train_data', type=str, default='data/transfer_train', help='transfer train data')
    parser.add_argument('transfer_test_data', type=str, default='data/transfer_test', help='transfer train data')
    parser.add_argument('model_path', type=str, default='ckpt', help='path to save model')
    parser.add_argument('demo_model_path', type=str, default='20200121', help='path to call demo model')
    parser.add_argument('map_path', type=str, default='data/maps.pkl', help='path to save maps')
    parser.add_argument('wiki_path', type=str, default='data/wiki_100.utf8', help='wiki chinese embeddings')
    parser.add_argument('tag2label_path', type=str, default='data/tag2label.json', help='config tag2label')
    parser.add_argument('transfer_tag2label_path', type=str, default='data/transfer_tag2label.json', help='config transfer tag2label')
    args = parser.parse_args()
    print(args)

    import pickle
    with open('./chat_module/ner/maps.pkl', 'rb') as fr:
        info = pickle.load(fr)
        char2id = info[0]
        id2char = info[1]
        transfer_tag2id = info[4]
        transfer_id2tag = info[5]

    ### find the latest demo model
    demo_path = os.path.join("./chat_module/ner/", args.demo_model_path) + "/"
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
        demo_transfer_test_manager = BatchManager(demo_transfer_test_data, args.batch_size)
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

    print(f"NER RES = {ret}")
    return ret


def ques_and_ans(ent_q, ent_a):
    ret = {
            "product_name": [], "time": [], "person_name": [], "org_name": [],
            "company_name": [], "location": [], "event": [],
          }

    for key in ret:
        ret[key] = (ent_q[key] + ent_a[key])

    return ret
