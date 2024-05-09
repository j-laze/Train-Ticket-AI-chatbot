import datetime

from utils import *
import webscrape.splitmyfare as splitmyfare

# tomorrow = (datetime.date.today() + datetime.timedelta(days=1))
# tomorrow_date_string = tomorrow.strftime("%Y-%m-%d")
# print(tomorrow_date_string)
# exit()

tomorrow = (datetime.date.today() + datetime.timedelta(days=1))

valid_start_alpha3  = "NRW"
valid_end_alpha3    = "LST"
valid_out_time      = "12:00"
valid_out_date      = tomorrow.strftime("%Y-%m-%d")
valid_ret_time      = "20:00"
valid_ret_date      = (tomorrow + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


valid_enquiry_strings_objects = [
    (
        "NRW to LST, single, out-depart after mid-day tomorrow, 1 adult",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.SINGLE,
            out_time_condition  = TimeCondition.DEPART_AFTER,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            adults              = 1,
        )
    ),
    (
        "NRW to LST, single, out-arrive before mid-day tomorrow, 1 adult, 1 child",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.SINGLE,
            out_time_condition  = TimeCondition.ARRIVE_BEFORE,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            adults              = 1,
            children            = 1,
        )
    ),
    (
        "NRW to LST, return, out-depart after mid-day tomorrow, ret-depart after 8pm the day after tomorrow, 1 adult",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.RETURN,
            out_time_condition  = TimeCondition.DEPART_AFTER,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            ret_time_condition  = TimeCondition.DEPART_AFTER,
            ret_time            = valid_ret_time,
            ret_date            = valid_ret_date,
            adults              = 1,
        )
    ),
    (
        "NRW to LST, return, out-arrive before mid-day tomorrow, ret-depart after 8pm the day after tomorrow, 1 adult",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.RETURN,
            out_time_condition  = TimeCondition.ARRIVE_BEFORE,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            ret_time_condition  = TimeCondition.DEPART_AFTER,
            ret_time            = valid_ret_time,
            ret_date            = valid_ret_date,
            adults              = 1,
        )
    ),
    (
        "NRW to LST, return, out-depart after mid-day tomorrow, ret-arrive before 8pm the day after tomorrow, 1 adult",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.RETURN,
            out_time_condition  = TimeCondition.DEPART_AFTER,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            ret_time_condition  = TimeCondition.ARRIVE_BEFORE,
            ret_time            = valid_ret_time,
            ret_date            = valid_ret_date,
            adults              = 1,
        )
    ),
    (
        "NRW to LST, return, out-arrive before mid-day tomorrow, ret-arrive before 8pm the day after tomorrow, 1 adult",
        Enquiry(
            start_alpha3        = valid_start_alpha3,
            end_alpha3          = valid_end_alpha3,
            journey_type        = JourneyType.RETURN,
            out_time_condition  = TimeCondition.ARRIVE_BEFORE,
            out_time            = valid_out_time,
            out_date            = valid_out_date,
            ret_time_condition  = TimeCondition.ARRIVE_BEFORE,
            ret_time            = valid_ret_time,
            ret_date            = valid_ret_date,
            adults              = 1,
        )
    ),
]



def test_splitmyfare_get_search_url():

    print()
    for enquiry_string, enquiry_object in valid_enquiry_strings_objects:
        print(enquiry_string)
        try:
            url = splitmyfare.get_search_url(enquiry_object)
        except Exception as e:
            print(e)
            continue
        print(url)
        print()



if __name__ == "__main__":
    test_splitmyfare_get_search_url()

