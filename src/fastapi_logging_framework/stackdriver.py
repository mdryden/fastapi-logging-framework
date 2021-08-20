
from typing import Dict
from .logger import Logger
from google.cloud.logging_v2.client import Client
from google.cloud.logging_v2.resource import Resource


class StackDriverLogger(Logger):
    def __init__(self, project_id, service_name, region):
        self.client = Client(project=project_id)
        self.project_id = project_id
        self.service_name = service_name
        self.region = region

    def __get_resource(self):
        return Resource(
            type="cloud_run_revision",
            labels={
                "project_id": self.project_id,
                "service_name": self.service_name,
                "location": self.region,
            })

    def __log(self, severity: str, message: str, extra: Dict = None, exc_info=None):
        trace = self.get_trace_id()

        if extra or exc_info:
            struct = {"message": message}

            if extra:
                struct["extra"] = extra

            if exc_info:
                struct["exception"] = exc_info
                struct["serviceContext"] = {
                    "service": self.service_name
                }
                struct["@type"] = "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent"

            self.client.logger(self.service_name).log_struct(struct, severity=severity, resource=self.__get_resource(), trace=trace)
        else:
            self.client.logger(self.service_name).log_text(message, severity=severity, resource=self.__get_resource(), trace=trace)

    def debug(self, message: str, extra: Dict = None):
        self.__log("DEBUG", message, extra=extra)

    def info(self, message: str, extra: Dict = None):
        self.__log("INFO", message, extra)

    def warn(self, message: str, extra: Dict = None):
        self.__log("WARNING", message, extra)

    def error(self, message: str, extra: Dict = None, exc_info=None):
        self.__log("ERROR", message, extra=extra, exc_info=exc_info)
