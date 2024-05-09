import datetime

from utils import *
import webscrape.splitmyfare as splitmyfare


tomorrow = (datetime.date.today() + datetime.timedelta(days=1))

valid_start_alpha3  = "NRW"
valid_end_alpha3    = "LST"
valid_out_time      = "12:00"
valid_out_date      = tomorrow.strftime("%Y-%m-%d")
valid_ret_time      = "20:00"
valid_ret_date      = (tomorrow + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


valid_enquiry_tuplist_desc_obj_url = [
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
            children            = 0
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate={valid_out_date}T{valid_out_time}"
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
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=1&departureDate={valid_out_date}T{valid_out_time}&departureBefore=1"
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
            children            = 0,
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate={valid_out_date}T{valid_out_time}&returnDate={valid_ret_date}T{valid_ret_time}"
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
            children            = 0,
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate={valid_out_date}T{valid_out_time}&departureBefore=1&returnDate={valid_ret_date}T{valid_ret_time}"
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
            children            = 0,
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate={valid_out_date}T{valid_out_time}&returnDate={valid_ret_date}T{valid_ret_time}&returnBefore=1"
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
            children            = 0,
        ),
        f"https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=0&departureDate={valid_out_date}T{valid_out_time}&departureBefore=1&returnDate={valid_ret_date}T{valid_ret_time}&returnBefore=1"
    ),
]



def test_splitmyfare_get_search_url():
    print()
    for description, enquiry, valid_url in valid_enquiry_tuplist_desc_obj_url:
        print(f"| DESCRIPTION  | {description}")
        try:
            result_url = splitmyfare.get_search_url(enquiry)
        except Exception as e:
            print(e)
            continue
        print(f"| EXPECTED URL | {valid_url}")
        print(f"| RESULT URL   | {result_url}")
        print(f"| TEST RESULT  | {'PASSED' if result_url == valid_url else 'FAILED'}")
        print()

def test_splitmyfare_get_journeys():
    # url = "https://book.splitmyfare.co.uk/search?from=7073090&to=7069650&adults=1&children=None&departureDate=2024-05-11T12:00"
    # journeys = splitmyfare.OLD_get_journeys(url)

    print()
    for description, enquiry, _ in valid_enquiry_tuplist_desc_obj_url:
        print(f"| DESCRIPTION  | {description}")
        try:
            journeys = splitmyfare.get_journeys(enquiry)
        except Exception as e:
            print(e)
            continue
        print(f"| TEST RESULT  | {'PASSED' if journeys else 'FAILED'}")
        print()

if __name__ == "__main__":
    # test_splitmyfare_get_search_url()
    test_splitmyfare_get_journeys()

    