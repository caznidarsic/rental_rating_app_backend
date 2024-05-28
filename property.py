from flask import Blueprint, jsonify, request
import psycopg2
import psycopg2.extras

# This file defines all endpoints with the prefix '/property'

property_bp = Blueprint('property', __name__, url_prefix='/property')


def get_db_connection():
    conn = psycopg2.connect(
        dbname="rental_rating_db",
        user='postgres',
        password='pgpassword',
        host="localhost",
        port="5432"
    )
    return conn


# Endpoint to return data for a given property
@property_bp.route("/", methods=['GET'])
def getProperty():
    nom_id = request.args.get('nom_id')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        'SELECT nom_id, lat, long, display_name, date_added FROM property WHERE nom_id = %s;', [nom_id])
    properties = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(properties)


# Endpoint to return all reviews for a given property
@property_bp.route("/reviews", methods=['GET'])
def getReviews():
    nom_id = request.args.get('nom_id')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        'SELECT review.property_id, review.content, review.date_added FROM review JOIN property ON review.property_id = property.id WHERE property.nom_id = %s;', [nom_id])
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(reviews)


# Endpoint to return all properties within specified coordinate box
@property_bp.route("/coordinates", methods=['GET'])
def getProperties():
    minLat, maxLat, minLong, maxLong = (request.args.get(
        param) for param in ('minLat', 'maxLat', 'minLong', 'maxLong'))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if (minLong > maxLong):  # Handle the case where the coordinate box is on the antimeridian
        cur.execute(
            'SELECT nom_id, lat, long, display_name, date_added FROM property WHERE lat > %s AND lat < %s AND ((long > %s AND long < 180) OR (long > -180 AND long < %s));', [minLat, maxLat, minLong, maxLong])
    else:
        cur.execute(
            'SELECT nom_id, lat, long, display_name, date_added FROM property WHERE lat > %s AND lat < %s AND long > %s AND long < %s;', [minLat, maxLat, minLong, maxLong])
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(reviews)


# Endpoint to create a new property
@property_bp.route("/", methods=['POST'])
def createProperty():
    nom_id, lat, long, display_name = (request.form.get(
        param) for param in ('nom_id', 'lat', 'long', 'display_name'))
    print(display_name)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            'INSERT INTO property (nom_id, lat, long, display_name) VALUES (%s, %s, %s, %s);', [nom_id, lat, long, display_name])
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cur.close()
    conn.close()
    return "Successfully added property."
