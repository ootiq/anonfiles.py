from __future__ import annotations
from .resp import ErrorResp, SuccessRespData
import requests


API_URL = "https://api.anonfiles.com"


class AnonFiles:
    """
    AnonFiles.com file hosting
    """

    def __init__(self, token: str = None) -> None:
        """
        Create new client.

        token: user api token
        """

        # URL Docs: https://anonfiles.com/docs/api

        self.__api_upload_url = API_URL + "/upload"  # UPLOAD api
        if token:
            self.__api_upload_url += f"?token={token}"
        self.__info_url = API_URL + "/v2/file/{id}/info"  # INFO api

    def upload(self, file: str) -> AnonSuccessResponse | AnonErrorResponse:
        """
        Upload file.

        file: (string) path of the file to upload
        """

        # TODO: implement multiple files

        # request
        with open(file, "rb") as f:
            r = requests.post(self.__api_upload_url, files={"file": f})

        # error response
        if not r.json()["status"]:
            return AnonErrorResponse(r.json())

        # success response
        return AnonSuccessResponse(r.json())

    def info(self, id: str) -> AnonSuccessResponse | AnonErrorResponse:
        """
        Grab info about a file.

        id: (string) file id
        """
        # TODO: implement multiple id

        # request
        r = requests.get(self.__info_url.format(id=id))

        # error response
        if not r.ok:
            return AnonErrorResponse(r.json())

        # success response
        return AnonSuccessResponse(r.json())


class BayFiles(AnonFiles):
    """
    BayFiles.com file hosting.
    """

    API_URL = "https://api.bayfiles.com"


class AnonSuccessResponse:
    def __init__(self, json: dict) -> None:
        self.status = json.get("status")
        self.data = SuccessRespData(json["data"])

    def __repr__(self) -> str:
        return f"\nSuccessfully uploaded `{self.data.file.metadata.name}` => {self.data.file.url.short}"


class AnonErrorResponse:
    def __init__(self, json: dict) -> None:
        self.status = json.get("status")
        self.error = ErrorResp(json["error"])

    def __repr__(self) -> str:
        return f"\nUpload Failed | {self.error.code} - {self.error.message}"
