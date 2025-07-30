from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
import zipfile
import os
import tempfile
import requests
from datetime import datetime
import json
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
try:
    client = MongoClient('mongodb+srv://infostylicai:gUgH6G9oDimFRWIS@stylicai.tio3ghn.mongodb.net/')  # Update with your MongoDB connection string
    db = client['stylic']  # Update with your database name
    collection = db['photoshoot_data']  # Update with your collection name

    # Test connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    collection = None


@app.route('/')
def index():
    return render_template('gallery.html')


@app.route('/photoshoot/<photoshoot_id>')
def photoshoot_detail(photoshoot_id):
    return render_template('photoshoot_detail.html', photoshoot_id=photoshoot_id)


@app.route('/api/photoshoot/<photoshoot_id>')
def get_photoshoot_detail(photoshoot_id):
    try:
        if collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not available'
            }), 500

        # Find photoshoot by photoshoot_id
        photoshoot = collection.find_one({'photoshoot_id': photoshoot_id})

        if not photoshoot:
            return jsonify({
                'success': False,
                'error': 'Photoshoot not found'
            }), 404

        # Convert ObjectId to string and format data
        photoshoot['_id'] = str(photoshoot['_id'])

        # Handle different datetime formats
        if 'created_at' in photoshoot:
            if isinstance(photoshoot['created_at'], dict) and '$date' in photoshoot['created_at']:
                photoshoot['created_at'] = photoshoot['created_at']['$date']
            elif hasattr(photoshoot['created_at'], 'isoformat'):
                photoshoot['created_at'] = photoshoot['created_at'].isoformat()

        # Ensure all_images is a list
        if 'all_images' in photoshoot and not isinstance(photoshoot['all_images'], list):
            photoshoot['all_images'] = []

        # Handle selected_poses if it's not properly formatted
        if 'selected_poses' in photoshoot and isinstance(photoshoot['selected_poses'], list):
            cleaned_poses = []
            for pose in photoshoot['selected_poses']:
                if isinstance(pose, str):
                    cleaned_pose = pose.replace('[', '').replace(']', '').replace('"', '').split(',')
                    cleaned_poses.extend([p.strip() for p in cleaned_pose if p.strip()])
            photoshoot['selected_poses'] = cleaned_poses

        return jsonify({
            'success': True,
            'data': photoshoot
        })

    except Exception as e:
        print(f"Error in get_photoshoot_detail: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/photoshoots')
def get_photoshoots():
    try:
        if collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not available'
            }), 500

        # Get filter parameters
        status = request.args.get('status', 'all')
        garment_type = request.args.get('garment_type', 'all')
        gender = request.args.get('gender', 'all')
        age_group = request.args.get('age_group', 'all')

        # Build query
        query = {}
        if status != 'all':
            query['status'] = status
        if garment_type != 'all':
            query['upload_garment_type'] = garment_type
        if gender != 'all':
            query['gender'] = gender
        if age_group != 'all':
            query['age_group'] = age_group

        print(f"MongoDB query: {query}")  # Debug print

        # Get data from MongoDB
        photoshoots = list(collection.find(query).sort('created_at', -1))
        print(f"Found {len(photoshoots)} photoshoots")  # Debug print

        # Convert ObjectId to string and format data
        for photoshoot in photoshoots:
            photoshoot['_id'] = str(photoshoot['_id'])

            # Handle different datetime formats
            if 'created_at' in photoshoot:
                if isinstance(photoshoot['created_at'], dict) and '$date' in photoshoot['created_at']:
                    photoshoot['created_at'] = photoshoot['created_at']['$date']
                elif hasattr(photoshoot['created_at'], 'isoformat'):
                    photoshoot['created_at'] = photoshoot['created_at'].isoformat()

            # Ensure all_images is a list
            if 'all_images' in photoshoot and not isinstance(photoshoot['all_images'], list):
                photoshoot['all_images'] = []

            # Handle selected_poses if it's not properly formatted
            if 'selected_poses' in photoshoot and isinstance(photoshoot['selected_poses'], list):
                # Clean up selected_poses format
                cleaned_poses = []
                for pose in photoshoot['selected_poses']:
                    if isinstance(pose, str):
                        # Remove brackets and quotes, split by comma
                        cleaned_pose = pose.replace('[', '').replace(']', '').replace('"', '').split(',')
                        cleaned_poses.extend([p.strip() for p in cleaned_pose if p.strip()])
                photoshoot['selected_poses'] = cleaned_poses

        return jsonify({
            'success': True,
            'data': photoshoots,
            'total': len(photoshoots)
        })

    except Exception as e:
        print(f"Error in get_photoshoots: {str(e)}")  # Debug print
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<photoshoot_id>')
def download_single_image(photoshoot_id):
    try:
        image_url = request.args.get('url')
        if not image_url:
            return jsonify({'error': 'Image URL required'}), 400

        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(response.content)
            temp_file.close()

            # Get filename from URL
            filename = os.path.basename(image_url)

            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype='image/png'
            )
        else:
            return jsonify({'error': 'Failed to download image'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-all/<photoshoot_id>')
def download_all_images(photoshoot_id):
    try:
        # Get photoshoot data
        photoshoot = collection.find_one({'photoshoot_id': photoshoot_id})
        if not photoshoot:
            return jsonify({'error': 'Photoshoot not found'}), 404

        # Create temporary zip file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()

        with zipfile.ZipFile(temp_zip.name, 'w') as zip_file:
            for i, image_url in enumerate(photoshoot.get('all_images', [])):
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        filename = f"image_{i + 1}_{os.path.basename(image_url)}"
                        zip_file.writestr(filename, response.content)
                except Exception as e:
                    print(f"Error downloading image {image_url}: {e}")
                    continue

        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name=f"photoshoot_{photoshoot_id}.zip",
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/filters')
def get_filters():
    try:
        if collection is None:
            return jsonify({
                'statuses': ['completed', 'processing', 'failed'],
                'garment_types': ['upper_garment', 'lower_garment'],
                'genders': ['male', 'female'],
                'age_groups': ['child', 'teen', 'young-adult', 'adult']
            })

        # Get unique values for filters
        statuses = list(collection.distinct('status'))
        garment_types = list(collection.distinct('upload_garment_type'))
        genders = list(collection.distinct('gender'))
        age_groups = list(collection.distinct('age_group'))

        return jsonify({
            'statuses': [s for s in statuses if s],  # Filter out None/empty values
            'garment_types': [g for g in garment_types if g],
            'genders': [g for g in genders if g],
            'age_groups': [a for a in age_groups if a]
        })
    except Exception as e:
        print(f"Error in get_filters: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)