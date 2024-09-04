from equiwatt_api.utils import clicolors


class EquiwattAPIException(Exception):
    def __init__(self, message: str, status_code: int = None, details: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        if self.status_code:
            return f"{clicolors.BOLD}code {self.status_code}: {clicolors.FAIL}{self.message}"
        return self.message

    @staticmethod
    def from_response(response):
        try:
            error_data = response.json()
            error_message = error_data.get("message", "Unknown error")
            error_details = error_data.get("error", "No details available")
        except ValueError:
            error_message = response.text
            error_details = "No details available"
        return EquiwattAPIException(
            message=error_message,
            status_code=response.status_code,
            details=error_details
        )
