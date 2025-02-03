OTP_EXPIRED = {
        "success": False,
            "data": {
                "message": "otp verification failed."
            }
    } 

OTP_VERIFICATION_FAILED = {
    'success': False,
    'data': {
        'message': 'OTP Verification Failed. Try again.'
    }
}

DATA_NOT_PROVIDED = {
    "success": False,
        "data": {
        "message": "Data not provided.",
        }
    }

MOBILE_NUMBER_NOT_PROVIDED = {
    "success": False,
        "data": {
        "message": "Mobile number not provided",
        }
    }
PASSWORD_NOT_PROVIDED = {
    "success": False,
        "data": {
        "message": "Password not provided",
        }
    }

SEND_OTP_FAILURE = {
    'success': False,
    'data': {
        'message': 'Failed to send OTP. Try again.',
    }
}

INVALID_MOBILE_NUMBER = {
    'success': False,
    'data': {
        'message': 'Invalid Mobile number.',
    }
}
INVALID_EMAIL_ID = {
    'success': False,
    'data': {
        'message': 'Invalid Email Id.',
    }
}

MOBILE_NO_EXISTS = {
    'success' : False,
    'data' : {
        'message' : 'User Exists With This Mobile Number. Please try With Another Mobile Number.'
    }
}

USER_TYPE_NOT_PROVIDED = {
    'success' : False,
    'data' : {
        'message' : 'User Type Not Provided.'
    }
}

USER_TYPE_NOT_PROVIDED = {
    'success' : False,
    'data' : {
        'message' : 'User Type Not Provided.'
    }
}

INVALID_USER_TYPE = {
    "success": False,
    "data": {
        "message": "Sorry, we are not allowing this user type.",
    }
}

USER_EXISTS = {
    "success": False,
    "data": {
        "message": "User already exists.",
    }
}

INVALID_EMAIL_ID = {
    'success': False,
    'data': {
        'message': 'Invalid email id.',
    }
}

REGISTRATION_COMPLETED = {
    'success': True,
    'data': {
        'message': 'Registration Completed Successfully.',
    }
}

OTP_SEND_SUCCESSFULLY = {
    'success': True,
    'data': {
        'message': 'OTP Send Successfully.',
    }
}

DATA_NOT_FOUND = {
    "success": False,
    "data": {
        "message": "Data not found",
    }
}

SOMETHING_WENT_WRONG = {
    "success": False,
    "data": {
        "message": "Unable to process the request at this moment.",
    }
}
APPOINTMENT_CREATED = {
    "success": True,
    "data": {
        "message": "Appointment Schedule Successfully.",
    }
}

LOGOUT_MESSAGE = {
    'success': True,
    'data': {
        'message': 'Successfully logged out.'
    }
}

AUTH_TOKEN_FAILURE = {
    'success': False,
    'data': {
        'message': 'Authorization token failure.',
        'status_code': 39
    }
}

ACCOUNT_IS_DEACTIVATED = {
    'success': False,
    'data': {
        'message': 'Your account is inactive please contact your do re-registration.',
    }
}
PASSWORD_NOT_PROVIDED = {
    'success': False,
    'data': {
        'message': 'You have not been provided password.',
    }
}

CONFIRM_PASSWORD_NOT_PROVIDED = {
    'success': False,
    'data': {
        'message': 'You have not been provided confirm password.',
    }
}

BOTH_PASSWORD_NOT_MATCHED = {
    'success': False,
    'data': {
        'message': 'Your password have not been matched with confirm password.',
    }
}

INVALID_PASSWORD = {
        "success": False,
        "data": {
            "message": "Password should be Min. 7 Characters, Should contain one number, one uppercase character, one lowercase character, one special character."
        }
    }

PAYMENT_VERIFICATION_FAILED = {
    'success': False,
    'data': {
        'message': 'Payment verification failed.',
        'error_code': 118
    }

}
DATA_INSERTED = {
    'success': True,
    'data': {
        'message': 'Data saved successfully'
    }
}
DATA_UPDATED = {
    'success': True,
    'data': {
        'message': 'Data updated successfully'
    }
}

APPOINTMENT_DELETE = {
    "success": True,
    "data": {
        "message": "Appoinment deleted successfully.",
    }

}

INVALID_REQUEST = {
    'success': False,
    'data': {
        'message': 'Invalid Request.',
        'status_code': 60
    }
}

UNREGISTERED_USER = {
    'success': False,
    'data': {
        'message': 'You are not a registered user. Please registration first and then try to login.',
        'status_code': 65
    }
}
PASSWORD_NOT_SET = {
    'success': False,
    'data': {
        'message': 'You have not set your password. Please set your password then try to login.',
        'status_code': 65
    }
}

INVALID_CREDENTIALS = {
    'success': False,
    'data': {
        'message': 'Invalid username or password.',
        'status_code': 20
    }
}

EMAIL_EXISTS = {
    "success": True,
    "data": {
        "msg": "The Email Id Already Exists."
    }
}
DOCTOR_NOT_FOUND = {
    "success": True,
    "data": {
        "msg": "The Doctor record not found."
    }
}
PATIENT_NOT_FOUND = {
    "success": True,
    "data": {
        "msg": "The Patient record not found."
    }
}

DOCTOR_DETAIL_NOT_PROVIDED = {
    "success": True,
    "data": {
        "msg": "Doctor Detail Not Provided."
    }
}

PATIENT_DETAIL_NOT_PROVIDED = {
    "success": True,
    "data": {
        "msg": "Patient Detail Not Provided."
    }
}

EMAIL_SENT = {
    'success': True,
    'data': {
        'message': 'Email sent successfully.',
    }
}

SEND_EMAIL_FAILURE = {
    'success': False,
    'data': {
        'message': 'Failed to send email. Try again.',
    }
}

UNAUTHORIZE_FOR_ADDING_STAFF = {
    'success': False,
    'data': {
        'message': 'You are Un-Autohrize for creating staff account.Doctor can have create staff account.',
    }
}

STAFF_ACCOUNT_CREATED = {
    'success': False,
    'data': {
        'message': 'Staff acoount created Successfully.',
    }
}

UNAUTHORIZE_FOR_SEE_STAFF_RECORDS = {
    'success': False,
    'data': {
        'message': 'Only Doctor can see their staff records.',
    }
}
UNAUTHORIZE = {
    'success': False,
    'data': {
        'message': 'Sorry You are not authorize for this activity.',
    }
}

RECORD_DELETED = {
    "success": True,
    "data": {
        "msg": "Record Deleted Successfully."
    }
}

MOBILE_NUMBER_OR_EMAIL_ID = {
    "success": False,
        "data": {
        "message": "Please provide Either Mobile Number or Email Id.",
        }
    }
GENERIC_API_FAILURE = {
    "success": False,
    "data": {
        "msg": "We are unable to process your request at this moment. Please try after sometime.",
    }
}

ACCOUNT_DELETED = {
    'success': True,
    'data': {
        'message': 'Your Account Deleted Successfully.'
    }
}
ACTION_TYPE_NOT_PROVIDED = {
    'success': True,
    'data': {
        'message': 'Action Type Not Provided.'
    }
}

USER_NOT_REGISTERED = {
    "success": False,
    "data": {
        "msg": "You are not registered. Please do registration first then try again",
    }

}
DATA_ALREADY_EXISTS = {
    "success": False,
    "data": {
        "msg": "Data already exists",
    }

}
APPOINTMENT_RECORD_NOT_FOUND = {
    "success": False,
    "data": {
        "msg": "The appointment record was not found",
    }

}
PAYMENT_SUCCESS = {
    "success": True,
    "data": {
        "msg": "Payment successfully received!",
    }

}