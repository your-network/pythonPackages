
def imageProcessing(data: dict,
                    type:str="product") -> dict:

    image_dic = {'images': {}}
    if type == "product":
        ## ThumbPic search
        if data.get("images"):
            for image in data["images"]:
                ## extra resolutions processing
                if image.get("extraResolutions"):
                    for extra_image in image["extraResolutions"]:
                        if extra_image.get("imageType") and extra_image.get("path"):
                            image_type = extra_image["imageType"].lower()
                            if image_type == "thumbnail" or image_type == "thumbpic":
                                image_dic['images'].update({"thumb": extra_image['path']})
                            elif image_type == "small":
                                image_dic['images'].update({"small": extra_image['path']})
                            elif image_type == "medium":
                                image_dic['images'].update({"medium": extra_image['path']})
                            elif image_type == "large":
                                image_dic['images'].update({"large": extra_image['path']})
                            elif image_type == "original":
                                image_dic['images'].update({"original": extra_image['path']})

                    ## processing status and thumb
                    if image_dic['images'].get("thumb") == None:
                        image_dic['images'].update({"thumb": image_dic.get("original")})

                ## process when no extra resolutions
                elif image.get("path"):
                    image_dic['images'].update({"original": image['path']})
                    image_dic['images'].update({"thumb": image['path']})

                ## check if more images need to be processed or this image is correct
                if image_dic['images'].get("original"):
                    break
                else:
                    ## fallback
                    image_dic['images'].update({"original": image['path']})
                    image_dic['images'].update({"thumb": image['path']})
                    break

    elif type == "category" or type == "brand":
        if data.get("images"):
            for image in data["images"]:
                image_type = image["imageType"].lower()
                if image_type == "thumbnail" or image_type == "thumbpic":
                    image_dic['images'].update({"thumb": image['path']})
                elif image_type == "small":
                    image_dic['images'].update({"small": image['path']})
                elif image_type == "medium":
                    image_dic['images'].update({"medium": image['path']})
                elif image_type == "large":
                    image_dic['images'].update({"large": image['path']})
                elif image_type == "original":
                    image_dic['images'].update({"original": image['path']})
                elif image_type == "headerpic":
                    image_dic['images'].update({"large": image['path']})

            ## fallback
            if image_dic == {}:
                for image in data["images"]:
                    image_dic['images'].update({"thumb": image['path'],
                                                "original": image['path']})
                    break

    return image_dic
