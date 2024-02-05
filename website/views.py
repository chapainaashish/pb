from flask import Flask, render_template, request, flash, url_for, Blueprint, redirect
from flask_login import login_required, current_user
from .models import Image
from . import db
from serpapi import GoogleSearch
import json
import requests
from statistics import median
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import cv2
import numpy as np

views = Blueprint('views', __name__)

#function that converts a given image to url by uploading it to the imgbb
def upload_image_to_imgbb(image_path, api_key):
    """
    Uploads an image to imgbb and returns its URL.
    
    Args:
        image_path (str): The path to the image file.
        api_key (str): The API key for imgbb.

    Returns:
        str: The URL of the uploaded image.
    """
    url = "https://api.imgbb.com/1/upload"
    files = {"image": (image_path, open(image_path, "rb"))}
    params = {"key": api_key}

    response = requests.post(url, files=files, params=params)
    data = response.json()

    return data.get("data", {}).get("url")

class APIKeyError(Exception):
    """Custom exception for handling API key errors."""
    pass

#In this function we scraping the google lens results and calculating the median value
def calculate_median(google_lens_results):
    """
    Scrapes Google Lens results, calculates and returns the median value.

    Args:
        google_lens_results (dict): The results from a Google Lens search.

    Returns:
        tuple: Median value, corresponding link, and title. 
        Returns (None, None, None) if no valid data is found.
    """
    try:
        # Remove unnecessary keys from the response
        del google_lens_results['search_metadata']
        del google_lens_results['search_parameters']

        # Assuming google_lens_results is your JSON object
        json_data = json.dumps(google_lens_results, indent=2, ensure_ascii=False)
        data = json.loads(json_data)


        # List to store extracted data
        extracted_data = []

        # Function to recursively extract values from nested dictionaries
        def extract_values(obj):
            if isinstance(obj, dict):
                # Check if the current dictionary has "extracted_value"
                if "price" in obj:
                    # Extract necessary information
                    value = obj.get("price", {}).get("extracted_value")
                    if value:
                      link = obj.get("link")
                      if link is None:
                        link = "No link found"
                      currency = obj.get("price", {}).get("currency")
                      title = obj.get("title")
                      #print(value, ", ", link, ", ", currency)
                      # Convert to Euro if the currency is in dollars
                      if currency == "$":
                          value = value*0.9

                      if (currency =="$") or (currency =="€") or (currency =="EUR"): #accept ONLY euro and dollar
                        # Append the extracted data
                        extracted_data.append((value, link, title))

                # Continue recursively
                for key, value in obj.items():
                    extract_values(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_values(item)
                        
  
        # Start the extraction
        extract_values(data)
        if extracted_data:
            # Extract values, links and titles separately
            values, links, titles = zip(*extracted_data)
        else:
            return None, None, None

        # Calculate the median
        if values:
            median_value = round(median(values), 2)

            # Find the index of the closest value to the median
            closest_index = min(range(len(values)), key=lambda i: abs(values[i] - median_value))

            # Extract closest link and title
            closest_link = links[closest_index]
            closest_title = titles[closest_index]

            return median_value, closest_link, closest_title
        else:
            return None, None, None

    except KeyError as e:
        # Raise a custom exception for API key errors
        raise APIKeyError(str(e))

#function that compares with cv2 if a given image is already uploaded by the same user
def image_exist(image, images):
    """
    Checks if an image already exists in the user's uploads.

    Args:
        image (str): The filename of the image to check.
        images (list): List of user's images.

    Returns:
        bool: True if the image exists, False otherwise.
    """
    a = cv2.imread(f'uploads/{image}')
    print(f'uploads/{image}')
    for im in images:
        b = cv2.imread(f'uploads/{im.filename}')
        if np.all(a == b):
            return True
    return False

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    View function for the home page.
    Handles image upload and processing.
    """
    images = current_user.images
    uses_our_key = current_user.api_key == '04c839c94c3f50ebb6635faef3600fb053b96ee718edcc8512d09421d03f407f'
    message = f'You are currently using our shared API key. You have {current_user.api_key_uses} more uses.'

    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        try:
            if (not uses_our_key) or (current_user.api_key_uses > 0):
                filename = secure_filename(file.filename)
                image_path = f'uploads/{filename}'

                file.save(image_path)

                imgbb_api_key = 'bfa49ab58a9b7bf8f799a1fb9745cd4f'
                url = upload_image_to_imgbb(image_path, imgbb_api_key)

                api_key = current_user.api_key

                google_lens_params = {
                    'api_key': api_key,#'04c839c94c3f50ebb6635faef3600fb053b96ee718edcc8512d09421d03f407f',
                    'engine': 'google_lens',
                    'url': url,
                    'hl': 'en',
                }

                search = GoogleSearch(google_lens_params)
                google_lens_results = search.get_dict()

                median_value, link, title = calculate_median(google_lens_results)
                
                if uses_our_key:
                    # Update the API key uses counter
                    current_user.api_key_uses -= 1
                    db.session.commit()
                    message = f'You are currently using our shared API key. You have {current_user.api_key_uses} more uses.'

                if median_value:
                    images = current_user.images
                    exist = False
                    if image_exist(filename, images):
                        #flash('You have already uploaded this image. It will not be saved again.', category='info')
                        exist = True
                    else:
                        # Create a new Image object
                        new_image = Image(
                            url=url,
                            filename = filename,
                            mean_value=median_value,
                            link = link,
                            title = title,
                            user_id=current_user.id  # associate the image with the current user's ID
                        )

                        # Add the new Image object to the database and update the total of the user
                        db.session.add(new_image)
                        current_user.total = round(current_user.total + median_value, 2)
                        db.session.commit()
                        images = current_user.images
                
                flash('File successfully uploaded', category='success')
                return render_template('home.html', user=current_user, url=url, median_value=median_value, link=link, title = title, exist=exist, images=images, uses_our_key = uses_our_key, message = message)
            else:
                flash('You have exceeded the limit of API key uses. Please create your own API key.', category='error')
        except APIKeyError:
            # Handle API key error
            flash('Something went wrong. Please make sure your API key is correct.', category='error')
    return render_template('home.html', user=current_user, images = images, uses_our_key = uses_our_key, message = message)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    View function for the settings page.
    Handles user settings updates like username, password, and API key.
    """
    if request.method == 'POST':
        if 'change_username' in request.form:
            new_username = request.form.get('new_username')
            # Handle changing username
            if len(new_username) < 2:
                flash('Username must be greater than 1 character.', category='error')
            else:
                current_user.username = new_username
                db.session.commit()
                flash('Username changed successfully!', category='success')

        elif 'change_password' in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            # Handle changing password
            if not check_password_hash(current_user.password, current_password):
                flash('Incorrect current password. Password not changed.', category='error')
            elif len(new_password) < 7:
                flash('New password must be at least 7 characters.', category='error')
            else:
                current_user.password = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                flash('Password changed successfully!', category='success')

        elif 'change_api_key' in request.form:
            new_api_key = request.form.get('new_api_key')
            # Handle changing API key
            current_user.api_key = new_api_key
            db.session.commit()
            flash('API Key changed successfully!', category='success')

    return render_template("settings.html", user=current_user)