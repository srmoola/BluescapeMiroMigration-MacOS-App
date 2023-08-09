# Python Code (python 3.5+)


import requests
import time

"""
Required modules:
   requests 2.22.0
"""


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rgb_to_string(r, g, b):
    colorstring = "yellow"
    if r == 254 and g == 232 and b == 108:
        colorstring = "yellow"
    elif r == 51 and g == 142 and b == 255:
        colorstring = "blue"
    elif r == 89 and g == 212 and b == 180:
        colorstring = "green"
    elif r == 255 and g == 164 and b == 107:
        colorstring = "orange"
    elif r == 255 and g == 110 and b == 110:
        colorstring = "red"
    return colorstring


def getCenterPosition(position, size):
    return round(position + (size / 2))


def bluescapeShapeConvert(miro_shape):
    if "triangle" in miro_shape:
        return "triangle"
    elif "arrow" in miro_shape:
        return "right_arrow"
    elif "star" in miro_shape:
        return "star"
    elif "ellipse" in miro_shape:
        return "circle"
    else:
        return miro_shape


def uploadAssetFailure(x, y, height, width):
    # miro_payload = {
    #     "data": {"shape": "rectangle", "content": "missing asset"},
    #     "style": {
    #         "fillColor": rgb_to_hex(255, 0, 0),
    #     },
    #     "position": {"x": x, "y": y},
    #     "geometry": {"height": height, "width": width},
    # }
    # miro_response = requests.post(
    #     url=miro_shape_url, json=miro_payload, headers=miro_headers
    # )
    print("Asset cannot be migrated")
    return


# recursive call to not exceed 5 minutes link expiration time for images
def migrateImages(
    startCount,
    this_bluescape_API_version,
    this_bluescape_workspaceId,
    this_bluescape_portal,
    this_miro_image_url,
    this_miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + this_bluescape_API_version
        + "/workspaces/"
        + this_bluescape_workspaceId
        + "/elements?type=Image"
    )

    bluescape_the_request = requests.get(
        this_bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )
    start = time.time()
    bluescape_json_response = bluescape_the_request.json()
    count = 0
    isFirstLoop = True
    for data in bluescape_json_response["data"]:
        pastSeconds = time.time() - start
        if count >= startCount and pastSeconds < 250:
            allKeysValid = True
            ##if count >358 and count <365:
            bluescape_currentimageHeight = 100
            bluescape_currentimagewidth = 100
            bluescape_currentX = 100
            bluescape_currentY = 100
            try:
                bluescape_currentimageHeight = data["boundingBox"]["height"]
                bluescape_currentimagewidth = data["boundingBox"]["width"]
                bluescape_currentX = getCenterPosition(
                    data["transform"]["x"], bluescape_currentimagewidth
                )
                bluescape_currentY = getCenterPosition(
                    data["transform"]["y"], bluescape_currentimageHeight
                )
                bluescape_currentimageURL = data["asset"]["url"]
                bluescape_currentPreviewImageURL = data["preview"]["url"]
                miro_payload = {
                    "data": {"url": bluescape_currentimageURL},
                    "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                    "geometry": {"height": bluescape_currentimageHeight},
                }
            except KeyError as e:
                allKeysValid = False
            if allKeysValid:
                miro_response = requests.post(
                    url=this_miro_image_url,
                    json=miro_payload,
                    headers=this_miro_headers,
                )
                try:
                    response = miro_response.json()
                    if response["type"] == "error":
                        if response["status"] == 400:
                            miro_payload = {
                                "data": {"url": bluescape_currentPreviewImageURL},
                                "position": {
                                    "x": bluescape_currentX,
                                    "y": bluescape_currentY,
                                },
                                "geometry": {"height": bluescape_currentimageHeight},
                            }
                            miro_response = requests.post(
                                url=this_miro_image_url,
                                json=miro_payload,
                                headers=this_miro_headers,
                            )
                            response = miro_response.json()
                            if response["type"] == "error":
                                if response["status"] == 400:
                                    uploadAssetFailure(
                                        bluescape_currentX,
                                        bluescape_currentY,
                                        bluescape_currentimageHeight,
                                        bluescape_currentimagewidth,
                                    )
                            else:
                                print("Preview instead of Asset")
                            # print(miro_response)
                    print("\nUploaded Image ")
                    print(count)
                except:
                    uploadAssetFailure(
                        bluescape_currentX,
                        bluescape_currentY,
                        bluescape_currentimageHeight,
                        bluescape_currentimagewidth,
                    )
                    print("Unexpected error")
            else:
                uploadAssetFailure(
                    bluescape_currentX,
                    bluescape_currentY,
                    bluescape_currentimageHeight,
                    bluescape_currentimagewidth,
                )
                print("\nInvalid Bluescape input")
        elif pastSeconds > 250:
            if isFirstLoop:
                migrateImages(
                    count,
                    this_bluescape_API_version,
                    this_bluescape_workspaceId,
                    this_bluescape_portal,
                    this_miro_image_url,
                    this_miro_headers,
                )
                isFirstLoop = False
            exit
        count = count + 1
    return


# recursive call to not exceed 5 minutes link expiration time for Documents
def migrateDocuments(
    startCount,
    this_bluescape_API_version,
    this_bluescape_workspaceId,
    this_bluescape_portal,
    this_miro_document_url,
    this_miro_headers,
):
    bluescape_API_endpoint = (
        "/"
        + this_bluescape_API_version
        + "/workspaces/"
        + this_bluescape_workspaceId
        + "/elements?type=Document"
    )

    bluescape_the_request = requests.get(
        this_bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )
    start = time.time()
    bluescape_json_response = bluescape_the_request.json()
    count = 0
    isFirstLoop = True
    for data in bluescape_json_response["data"]:
        pastSeconds = time.time() - start
        if count >= startCount and pastSeconds < 250:
            bluescape_currentHeight = 100
            bluescape_currentWidth = 100
            bluescape_currentX = 100
            bluescape_currentY = 100
            try:
                bluescape_currentdocumentHeight = data["height"]
                bluescape_currentdocumentWidth = data["width"]
                bluescape_currentX = getCenterPosition(
                    data["transform"]["x"], bluescape_currentdocumentWidth
                )
                bluescape_currentY = getCenterPosition(
                    data["transform"]["y"], bluescape_currentdocumentHeight
                )
                bluescape_currentdocumentURL = data["asset"]["url"]
                miro_payload = {
                    "data": {"url": bluescape_currentdocumentURL},
                    "position": {
                        "origin": "center",
                        "x": bluescape_currentX,
                        "y": bluescape_currentY,
                    },
                    "geometry": {"height": bluescape_currentdocumentHeight},
                }
                miro_response = requests.post(
                    url=this_miro_document_url,
                    json=miro_payload,
                    headers=this_miro_headers,
                )
                response = miro_response.json()
                # print(miro_response)
                print("\nUploaded Document ")
                print(count)
            except:
                uploadAssetFailure(
                    bluescape_currentX,
                    bluescape_currentY,
                    bluescape_currentHeight,
                    bluescape_currentWidth,
                )
                print("Unexpected error")
        elif pastSeconds > 250:
            if isFirstLoop:
                migrateDocuments(
                    count,
                    this_bluescape_API_version,
                    this_bluescape_workspaceId,
                    this_bluescape_portal,
                    this_miro_document_url,
                    this_miro_headers,
                )
                isFirstLoop = False
            exit
        count = count + 1
    return


bluescape_token = "INSERT BLUESCAPE TOKEN HERE"

f = open("logs.txt", "w")


def mainCall(bluescape, miro):
    # print("\nWelcome to the Miro to Bluescape Migration Script\n")
    # print("powered by dfoerst5\n")
    print("\n \n")
    print(
        "###### Please add user madmin8@ford.com to bluescape and to miro board, otherwise script will not work ######"
    )
    bluescape_portal = "https://api.apps.us.bluescape.com"
    bluescape_workspaceId = bluescape
    #'ECBqXkhTJxQJdocaxXsY'
    bluescape_API_version = "v3"

    miro_workspace_ID = miro
    miro_image_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/images"
    )
    miro_text_url = "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/texts"
    miro_frame_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/frames"
    )
    miro_note_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/sticky_notes"
    )
    miro_shape_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/shapes"
    )
    miro_document_url = (
        "https://api.miro.com/v2/boards/" + miro_workspace_ID + "%3D/documents"
    )
    miro_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_3ZPvVnRBc146wIiLspMo3Guexl4",
    }

    ##################################################################Canvas section

    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Canvas"
    )

    bluescape_the_request = requests.get(
        bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )

    bluescape_json_response = bluescape_the_request.json()
    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currentWidth = 100
        bluescape_currentHeight = 100
        bluescape_currentX = 100
        bluescape_currentY = 100
        try:
            bluescape_currentWidth = data["style"]["width"]
            bluescape_currentHeight = data["style"]["height"]
            bluescape_currentX = getCenterPosition(
                data["transform"]["x"], bluescape_currentWidth
            )
            bluescape_currentY = getCenterPosition(
                data["transform"]["y"], bluescape_currentHeight
            )
            bluescape_currentcanvastitle = data["name"]
            bluescape_currentcolor = rgb_to_hex(
                data["style"]["fillColor"]["r"],
                data["style"]["fillColor"]["g"],
                data["style"]["fillColor"]["b"],
            )
            miro_payload = {
                "data": {"title": bluescape_currentcanvastitle},
                "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                "style": {
                    "fillColor": bluescape_currentcolor,
                },
                "geometry": {
                    "width": bluescape_currentWidth,
                    "height": bluescape_currentHeight,
                },
            }
            miro_response = requests.post(
                url=miro_frame_url, json=miro_payload, headers=miro_headers
            )
            print("\nUploaded Canvas ")
        except:
            uploadAssetFailure(
                bluescape_currentX,
                bluescape_currentY,
                bluescape_currentHeight,
                bluescape_currentWidth,
            )
        print(count)

    ##################################################################Image section

    migrateImages(
        0,
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        miro_image_url,
        miro_headers,
    )

    ##################################################################Text section

    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Text"
    )

    bluescape_the_request = requests.get(
        bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )

    bluescape_json_response = bluescape_the_request.json()
    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currentWidth = 100
        bluescape_currentHeight = 100
        bluescape_currentX = 100
        bluescape_currentY = 100
        try:
            bluescape_currentWidth = data["style"]["width"]
            bluescape_currentHeight = data["style"]["height"]
            bluescape_currentX = getCenterPosition(
                data["transform"]["x"], bluescape_currentWidth
            )
            bluescape_currentY = getCenterPosition(
                data["transform"]["y"], bluescape_currentHeight
            )
            bluescape_currenttextFontSize = data["style"]["fontSize"]
            bluescape_currenttext = data["text"]
            colorNotSet = True
            try:
                for subdata in data["blocks"]:
                    for subdata2 in subdata["content"]:
                        bluescape_currentcolor = rgb_to_hex(
                            subdata2["span"]["color"]["r"],
                            subdata2["span"]["color"]["g"],
                            subdata2["span"]["color"]["b"],
                        )
                        colorNotSet = False
            except TypeError as e:
                if colorNotSet:
                    bluescape_currentcolor = rgb_to_hex(
                        data["style"]["color"]["r"],
                        data["style"]["color"]["g"],
                        data["style"]["color"]["b"],
                    )
            except KeyError as e:
                if colorNotSet:
                    bluescape_currentcolor = rgb_to_hex(
                        data["style"]["color"]["r"],
                        data["style"]["color"]["g"],
                        data["style"]["color"]["b"],
                    )
            if data["style"]["backgroundColor"]["a"] != 0:
                bluescape_currentbackgroundcolor = rgb_to_hex(
                    data["style"]["backgroundColor"]["r"],
                    data["style"]["backgroundColor"]["g"],
                    data["style"]["backgroundColor"]["b"],
                )
                miro_payload = {
                    "data": {"content": bluescape_currenttext},
                    "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                    "style": {
                        "fontSize": bluescape_currenttextFontSize,
                        "color": bluescape_currentcolor,
                        "fillColor": bluescape_currentbackgroundcolor,
                    },
                    "geometry": {"width": bluescape_currentWidth},
                }
            else:
                miro_payload = {
                    "data": {"content": bluescape_currenttext},
                    "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                    "style": {
                        "fontSize": bluescape_currenttextFontSize,
                        "color": bluescape_currentcolor,
                    },
                    "geometry": {"width": bluescape_currentWidth},
                }
            miro_response = requests.post(
                url=miro_text_url, json=miro_payload, headers=miro_headers
            )
            # print(miro_response)
            print("\nUploaded Text ")
        except:
            uploadAssetFailure(
                bluescape_currentX,
                bluescape_currentY,
                bluescape_currentHeight,
                bluescape_currentWidth,
            )
        print(count)

    ##################################################################Notecard section

    bluescape_API_endpoint = (
        "/"
        + bluescape_API_version
        + "/workspaces/"
        + bluescape_workspaceId
        + "/elements?type=Shape"
    )

    bluescape_the_request = requests.get(
        bluescape_portal + bluescape_API_endpoint,
        headers={
            "Authorization": "Bearer " + bluescape_token,
            "Content-Type": "application/json",
        },
    )

    bluescape_json_response = bluescape_the_request.json()
    count = 0
    for data in bluescape_json_response["data"]:
        count = count + 1
        bluescape_currenttext = ""
        bluescape_currenttextcolor = rgb_to_hex(0, 0, 0)
        bluescape_currentfontsize = ""
        bluescape_currentWidth = 100
        bluescape_currentHeight = 100
        bluescape_currentX = 100
        bluescape_currentY = 100
        try:
            bluescape_currentWidth = data["style"]["width"]
            bluescape_currentHeight = data["style"]["height"]
            bluescape_currentX = getCenterPosition(
                data["transform"]["x"], bluescape_currentWidth
            )
            bluescape_currentY = getCenterPosition(
                data["transform"]["y"], bluescape_currentHeight
            )
            bluescape_currenttext = data["text"]
            bluescape_currentcolor = rgb_to_hex(
                data["style"]["fillColor"]["r"],
                data["style"]["fillColor"]["g"],
                data["style"]["fillColor"]["b"],
            )
            bluescape_currenttextcolor = rgb_to_hex(
                data["textStyle"]["color"]["r"],
                data["textStyle"]["color"]["g"],
                data["textStyle"]["color"]["b"],
            )
            try:
                for subdata in data["blocks"]:
                    for subdata2 in subdata["content"]:
                        bluescape_currentfontsize = subdata2["span"]["fontSize"]
            except TypeError as e:
                bluescape_currentfontsize = data["textStyle"]["fontSize"]
            except KeyError as e:
                bluescape_currentfontsize = data["textStyle"]["fontSize"]
            if (
                bluescape_currentWidth == bluescape_currentHeight
                and data["kind"] == "rectangle"
                or data["kind"] == "sticky-rectangle"
            ):
                #########Sticky note
                bluescape_currentcolor = rgb_to_string(
                    data["style"]["fillColor"]["r"],
                    data["style"]["fillColor"]["g"],
                    data["style"]["fillColor"]["b"],
                )
                miro_payload = {
                    "data": {"shape": "square", "content": bluescape_currenttext},
                    "style": {"fillColor": bluescape_currentcolor},
                    "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                    "geometry": {"width": bluescape_currentWidth},
                }
                miro_response = requests.post(
                    url=miro_note_url, json=miro_payload, headers=miro_headers
                )
                # print(miro_response)
                print("\nUploaded Note ")
                # print(count)
            #########Shape
            else:
                bluescape_shape = bluescapeShapeConvert(data["kind"])
                if type(bluescape_currentfontsize) == str:
                    bluescape_currentfontsize = "144"
                else:
                    bluescape_currentfontsize = round(int(bluescape_currentfontsize))
                    if bluescape_currentfontsize > 288:
                        bluescape_currentfontsize = "288"
                miro_payload = {
                    "data": {
                        "shape": bluescape_shape,
                        "content": bluescape_currenttext,
                    },
                    "style": {
                        "fontSize": bluescape_currentfontsize,
                        "fillColor": bluescape_currentcolor,
                        "color": bluescape_currenttextcolor,
                    },
                    "position": {"x": bluescape_currentX, "y": bluescape_currentY},
                    "geometry": {
                        "height": bluescape_currentHeight,
                        "width": bluescape_currentWidth,
                    },
                }
                miro_response = requests.post(
                    url=miro_shape_url, json=miro_payload, headers=miro_headers
                )
                print("\nUploaded Shape ")
        except:
            uploadAssetFailure(
                bluescape_currentX,
                bluescape_currentY,
                bluescape_currentHeight,
                bluescape_currentWidth,
            )
        print(count)

    ##################################################################Documents section

    migrateDocuments(
        0,
        bluescape_API_version,
        bluescape_workspaceId,
        bluescape_portal,
        miro_document_url,
        miro_headers,
    )
