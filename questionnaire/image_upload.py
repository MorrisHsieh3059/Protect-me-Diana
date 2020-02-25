from imgurpython import ImgurClient

class Image_Upload:
    def __init__(self, image_path):
        self.image_path = image_path

        # 小魚's imgur account
        self.client_id = 'a7cfb2393adac4f'
        self.client_secret = '1ea832c7844f4373e187ffc928219d847b28d2d4'
        self.access_token = 'bf4929e1f142dd8b3695fa6fa6029fc9a3e6ab4c'
        self.refresh_token = '41a031f77a90751b06064a1d7fc5669f8b8db010'

    def upload_photo(self):
        """
            Photo to imgur server return photo link
        """
        client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)
        album = None # You can also enter an album ID here
        config = { 'album': album }
        print("Uploading image...")
        image = client.upload_from_path(self.image_path, config=config, anon=False)
        print("Done")
        return image['link']
