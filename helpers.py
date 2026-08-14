import json
import time
from selenium.common import WebDriverException


def retrieve_phone_code(driver) -> str:
    """Obtiene el código de confirmación telefónica desde los logs de Chrome."""

    for _ in range(15):
        try:
            logs = driver.get_log("performance")

            for log in reversed(logs):
                try:
                    message = json.loads(log["message"])["message"]

                    if message["method"] != "Network.responseReceived":
                        continue

                    response = message["params"]["response"]
                    url = response.get("url", "")

                    if "api/v1/number?number" not in url:
                        continue

                    request_id = message["params"]["requestId"]

                    body = driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": request_id}
                    )

                    code = "".join(
                        x for x in body["body"] if x.isdigit()
                    )

                    if code:
                        return code

                except (KeyError, json.JSONDecodeError, WebDriverException):
                    continue

        except WebDriverException:
            pass

        time.sleep(1)

    raise Exception(
        "No se encontró el código de confirmación del teléfono."
    )