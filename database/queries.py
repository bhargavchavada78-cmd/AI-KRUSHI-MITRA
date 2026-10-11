from database.connection import get_connection

def add_farmer(name, mobile, language):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO farmers
    (name, mobile, language)
    VALUES (%s, %s, %s)
    """

    values = (name, mobile, language)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()



def get_farmers():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM farmers
    """

    cursor.execute(query)

    farmers = cursor.fetchall()

    cursor.close()
    connection.close()

    return farmers



def get_farmer(farmer_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM farmers
    WHERE farmer_id = %s
    """

    cursor.execute(query, (farmer_id,))

    farmer = cursor.fetchone()

    cursor.close()
    connection.close()

    return farmer



def update_farmer(farmer_id, name, mobile, language):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE farmers
    SET name = %s,
        mobile = %s,
        language = %s
    WHERE farmer_id = %s
    """

    values = (
        name,
        mobile,
        language,
        farmer_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()



def delete_farmer(farmer_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM farmers
    WHERE farmer_id = %s
    """

    cursor.execute(query, (farmer_id,))

    connection.commit()

    cursor.close()
    connection.close()





def add_crop(
    farm_id,
    crop_name,
    variety,
    sowing_date,
    irrigation_type
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO crops
    (farm_id, crop_name, variety, sowing_date, irrigation_type)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        farm_id,
        crop_name,
        variety,
        sowing_date,
        irrigation_type
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()



def get_crops():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM crops
    """

    cursor.execute(query)

    crops = cursor.fetchall()

    cursor.close()
    connection.close()

    return crops



def get_crop(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM crops
    WHERE crop_id = %s
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    cursor.close()
    connection.close()

    return crop



def update_crop(
    crop_id,
    crop_name,
    variety,
    sowing_date,
    irrigation_type
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE crops
    SET crop_name = %s,
        variety = %s,
        sowing_date = %s,
        irrigation_type = %s
    WHERE crop_id = %s
    """

    values = (
        crop_name,
        variety,
        sowing_date,
        irrigation_type,
        crop_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()



def delete_crop(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM crops
    WHERE crop_id = %s
    """

    cursor.execute(query, (crop_id,))

    connection.commit()

    cursor.close()
    connection.close()
    from database.connection import get_connection



def add_farm(farmer_id, location, area, soil_type):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO farms
    (farmer_id, location, area, soil_type)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (farmer_id, location, area, soil_type)
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_farms():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM farms")

    farms = cursor.fetchall()

    cursor.close()
    connection.close()

    return farms


def get_farm(farm_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM farms
    WHERE farm_id = %s
    """

    cursor.execute(query, (farm_id,))

    farm = cursor.fetchone()

    cursor.close()
    connection.close()

    return farm


def update_farm(farm_id, location, area, soil_type):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE farms
    SET location = %s,
        area = %s,
        soil_type = %s
    WHERE farm_id = %s
    """

    cursor.execute(
        query,
        (location, area, soil_type, farm_id)
    )

    connection.commit()

    cursor.close()
    connection.close()


def delete_farm(farm_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM farms
    WHERE farm_id = %s
    """

    cursor.execute(query, (farm_id,))

    connection.commit()

    cursor.close()
    connection.close()




def add_crop_image(crop_id, image_path):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO crop_images
    (crop_id, image_path)
    VALUES (%s, %s)
    """

    cursor.execute(query, (crop_id, image_path))

    connection.commit()

    cursor.close()
    connection.close()


def get_crop_images(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM crop_images
    WHERE crop_id = %s
    ORDER BY capture_date DESC
    """

    cursor.execute(query, (crop_id,))

    images = cursor.fetchall()

    cursor.close()
    connection.close()

    return images


def get_crop_image(image_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM crop_images
    WHERE image_id = %s
    """

    cursor.execute(query, (image_id,))

    image = cursor.fetchone()

    cursor.close()
    connection.close()

    return image


def delete_crop_image(image_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM crop_images
    WHERE image_id = %s
    """

    cursor.execute(query, (image_id,))

    connection.commit()

    cursor.close()
    connection.close()



def save_health_analysis(
    image_id,
    prediction,
    confidence,
    severity
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO health_analysis
    (image_id, prediction, confidence, severity)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        image_id,
        prediction,
        confidence,
        severity
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_health_analysis(image_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM health_analysis
    WHERE image_id = %s
    ORDER BY analysis_date DESC
    """

    cursor.execute(query, (image_id,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def get_latest_health_analysis(image_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM health_analysis
    WHERE image_id = %s
    ORDER BY analysis_date DESC
    LIMIT 1
    """

    cursor.execute(query, (image_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result




def add_weather(
    farm_id,
    weather_date,
    temperature,
    humidity,
    rainfall,
    rain_probability
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO weather
    (farm_id, weather_date, temperature, humidity,
     rainfall, rain_probability)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        farm_id,
        weather_date,
        temperature,
        humidity,
        rainfall,
        rain_probability
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_weather(farm_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM weather
    WHERE farm_id = %s
    ORDER BY weather_date DESC
    """

    cursor.execute(query, (farm_id,))

    weather = cursor.fetchall()

    cursor.close()
    connection.close()

    return weather


def get_latest_weather(farm_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM weather
    WHERE farm_id = %s
    ORDER BY weather_date DESC
    LIMIT 1
    """

    cursor.execute(query, (farm_id,))

    weather = cursor.fetchone()

    cursor.close()
    connection.close()

    return weather


def update_weather(
    weather_id,
    temperature,
    humidity,
    rainfall,
    rain_probability
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE weather
    SET temperature = %s,
        humidity = %s,
        rainfall = %s,
        rain_probability = %s
    WHERE weather_id = %s
    """

    values = (
        temperature,
        humidity,
        rainfall,
        rain_probability,
        weather_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def delete_weather(weather_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM weather
    WHERE weather_id = %s
    """

    cursor.execute(query, (weather_id,))

    connection.commit()

    cursor.close()
    connection.close()




def add_treatment(
    crop_id,
    problem,
    product,
    application_date,
    note
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO treatments
    (crop_id, problem, product, application_date, note)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        crop_id,
        problem,
        product,
        application_date,
        note
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_treatments(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM treatments
    WHERE crop_id = %s
    ORDER BY application_date DESC
    """

    cursor.execute(query, (crop_id,))

    treatments = cursor.fetchall()

    cursor.close()
    connection.close()

    return treatments


def update_treatment(
    treatment_id,
    problem,
    product,
    application_date,
    note
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE treatments
    SET problem = %s,
        product = %s,
        application_date = %s,
        note = %s
    WHERE treatment_id = %s
    """

    values = (
        problem,
        product,
        application_date,
        note,
        treatment_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def delete_treatment(treatment_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM treatments
    WHERE treatment_id = %s
    """

    cursor.execute(query, (treatment_id,))

    connection.commit()

    cursor.close()
    connection.close()



def add_fertilizer(
    crop_id,
    fertilizer_type,
    application_date,
    note
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO fertilizers
    (crop_id, fertilizer_type, application_date, note)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        crop_id,
        fertilizer_type,
        application_date,
        note
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_fertilizers(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM fertilizers
    WHERE crop_id = %s
    ORDER BY application_date DESC
    """

    cursor.execute(query, (crop_id,))

    fertilizers = cursor.fetchall()

    cursor.close()
    connection.close()

    return fertilizers


def update_fertilizer(
    fertilizer_id,
    fertilizer_type,
    application_date,
    note
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE fertilizers
    SET fertilizer_type = %s,
        application_date = %s,
        note = %s
    WHERE fertilizer_id = %s
    """

    values = (
        fertilizer_type,
        application_date,
        note,
        fertilizer_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def delete_fertilizer(fertilizer_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM fertilizers
    WHERE fertilizer_id = %s
    """

    cursor.execute(query, (fertilizer_id,))

    connection.commit()

    cursor.close()
    connection.close()



def add_activity(
    crop_id,
    activity,
    recommended_date,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO activities
    (crop_id, activity, recommended_date, status)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        crop_id,
        activity,
        recommended_date,
        status
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_activities(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM activities
    WHERE crop_id = %s
    ORDER BY recommended_date
    """

    cursor.execute(query, (crop_id,))

    activities = cursor.fetchall()

    cursor.close()
    connection.close()

    return activities


def update_activity(
    activity_id,
    activity,
    recommended_date,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE activities
    SET activity = %s,
        recommended_date = %s,
        status = %s
    WHERE activity_id = %s
    """

    values = (
        activity,
        recommended_date,
        status,
        activity_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def delete_activity(activity_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM activities
    WHERE activity_id = %s
    """

    cursor.execute(query, (activity_id,))

    connection.commit()

    cursor.close()
    connection.close()



def add_alert(
    crop_id,
    alert_type,
    message,
    severity,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO alerts
    (crop_id, alert_type, message, severity, status)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        crop_id,
        alert_type,
        message,
        severity,
        status
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def get_alerts(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM alerts
    WHERE crop_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(query, (crop_id,))

    alerts = cursor.fetchall()

    cursor.close()
    connection.close()

    return alerts


def update_alert(
    alert_id,
    alert_type,
    message,
    severity,
    status
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE alerts
    SET alert_type = %s,
        message = %s,
        severity = %s,
        status = %s
    WHERE alert_id = %s
    """

    values = (
        alert_type,
        message,
        severity,
        status,
        alert_id
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def delete_alert(alert_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM alerts
    WHERE alert_id = %s
    """

    cursor.execute(query, (alert_id,))

    connection.commit()

    cursor.close()
    connection.close()
def get_crop_status(crop_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        crop_id,
        crop_name,
        variety,
        sowing_date,
        DATEDIFF(CURDATE(), sowing_date) AS crop_age
    FROM crops
    WHERE crop_id = %s
    """

    cursor.execute(query, (crop_id,))

    crop = cursor.fetchone()

    cursor.close()
    connection.close()

    return crop
def get_crop_stage(crop_age):

    if crop_age < 20:
        return "Early Growth"

    elif crop_age < 50:
        return "Vegetative Growth"

    elif crop_age < 80:
        return "Flowering / Development"

    else:
        return "Mature / Late Stage"
def get_full_crop_status(crop_id):

    crop = get_crop_status(crop_id)

    if crop is None:
        return None

    crop_id = crop[0]
    crop_name = crop[1]
    variety = crop[2]
    sowing_date = crop[3]
    crop_age = crop[4]

    stage = get_crop_stage(crop_age)

    return {
        "crop_id": crop_id,
        "crop_name": crop_name,
        "variety": variety,
        "sowing_date": sowing_date,
        "crop_age": crop_age,
        "stage": stage
    }    