
from django_solvitize.utils.constants import DATA, MESSAGE, STATUS
from django_solvitize.utils.GlobalImports import *



def helloworld():
    print("Solvitize: Hello World")

def ResponseFunction(status, message, data):
    false_list = [0, "false", False, "0"]
    if status in false_list:
        status = False
    else:
        status = True

    return Response({
        STATUS: status,
        MESSAGE: message,
        DATA: data
    })


def ExcepctionResponseFunction(status, message, data, requestdata):
    from django_solvitize.ErrorApp.models import ErrorModel
    
    false_list = [0, "false", False, "0"]
    if status in false_list:
        status = False
    else:
        status = True

    ErrorModel.objects.create(
        title=message,
        body=data,
        data=str(requestdata),
    )

    return Response({
        STATUS: status,
        MESSAGE: message,
        DATA: data
    })


def printLineNo():
    return str(format(sys.exc_info()[-1].tb_lineno))


def excludeValidation(exculded, data_dic):
    errors = []
    print("Receved data ", data_dic)

    message = ""

    for field in exculded:
        print(f"checking {field} in data")
        if field in data_dic:
            message = f"Remove {field} from data body"
            errors.append({"error": message})
        else:

            print("Non required field found")

            # print(message)
        # print(f"Conclusion of {field} : ",message)
    print(errors)

    return errors


def ValidateRequest(required, data_dic, **kwargs):
    errors = []
    message = ""
    for field in required:
        if field not in data_dic:
            message = f"Required {field}"
            errors.append({"error": message})
        else:
            if data_dic[field] == "" or not data_dic[field]:
                message = f"{field} cannot be empty"
                errors.append({"error": message})
                # print(message)

            else:
                message = f"{field} found"
    if len(errors):
        'Print if there where errors'
        print(errors)
    return errors


def format_api_response(response):
    """
    Methos used to validate and format external api response.
    """

    try:
        response_data = response.json()
    except ValueError:
        response_data = response.text

    status_code = response.status_code
    bln_status = False
    message = None
    response_data = None

    if status_code >= 200 and status_code < 300:
        bln_status = True
        message = "Request Successful."
        data = response_data
    elif status_code == 400:
        message = "Bad Request: The server could not understand the request."
        if isinstance(response_data, dict) and "error" in response_data:
            data = response_data['error']
    elif status_code == 401:
        message = "Unauthorized: Invalid authentication credentials."
    elif status_code == 403:
        message = "Forbidden: You do not have permission to access this resource."
    elif status_code == 404:
        message = "Not Found: The requested resource could not be found."
    elif status_code == 500:
        message = "Internal Server Error: The server encountered an error."
    elif status_code == 503:
        message = "Service Unavailable: The server is temporarily unavailable."
    elif not status_code:
        message = f"HTTP {status_code}: Unexpected error."

    return {
        "status": bln_status,
        "message": message,
        "data": response_data,
    }
