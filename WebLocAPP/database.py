import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='locapp.db'):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database with all tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Table pour les propriétés (menu principal)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                icon TEXT DEFAULT '🏠',
                location TEXT,
                description TEXT,
                theme TEXT DEFAULT 'mazet-bsa',
                accent_color TEXT DEFAULT '#D4A574',
                is_active BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table pour les informations générales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS general_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                property_name TEXT NOT NULL,
                welcome_title TEXT,
                welcome_message TEXT,
                welcome_description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour WiFi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wifi_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                ssid TEXT NOT NULL,
                password TEXT NOT NULL,
                location_description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour l'adresse
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS address (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                street TEXT NOT NULL,
                postal_code TEXT NOT NULL,
                city TEXT NOT NULL,
                country TEXT DEFAULT 'France',
                description TEXT,
                latitude REAL,
                longitude REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour le parking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                distance TEXT,
                description TEXT,
                is_free BOOLEAN DEFAULT 1,
                tips TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les clés et accès
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                check_in_time TEXT DEFAULT '16:00',
                check_out_time TEXT DEFAULT '10:00',
                keybox_code TEXT,
                keybox_location TEXT,
                access_instructions TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les contacts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                host_name TEXT,
                phone TEXT NOT NULL,
                email TEXT,
                whatsapp TEXT,
                airbnb_url TEXT,
                description TEXT,
                response_time TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les numéros d'urgence
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                number TEXT NOT NULL,
                category TEXT DEFAULT 'emergency',
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les services à proximité
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nearby_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                icon TEXT,
                address TEXT,
                phone TEXT,
                description TEXT,
                opening_hours TEXT,
                latitude REAL,
                longitude REAL,
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les activités
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                emoji TEXT,
                distance TEXT,
                latitude REAL,
                longitude REAL,
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les catégories d'activités
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                icon TEXT,
                color TEXT,
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les équipements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS amenities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                icon TEXT,
                description TEXT,
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        # Table pour les instructions de départ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkout_instructions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                instruction TEXT NOT NULL,
                icon TEXT,
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id)
            )
        ''')

        conn.commit()

        # Migrer les données existantes et insérer les valeurs par défaut
        self._migrate_and_insert_default_data(cursor, conn)
        conn.close()

    def _migrate_and_insert_default_data(self, cursor, conn):
        """Migrate existing data and insert default data"""

        # Vérifier si les propriétés existent
        cursor.execute('SELECT COUNT(*) FROM properties')
        if cursor.fetchone()[0] == 0:
            # Créer la propriété Mazet BSA (Thème Orange Provence 🟠)
            cursor.execute('''
                INSERT INTO properties (name, slug, icon, location, description, theme, accent_color, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Mazet BSA',
                'mazet-bsa',
                '🏡',
                'Bourg-Saint-Andéol, Ardèche',
                'Le Mazet de Bourg-Saint-Andéol',
                'mazet-bsa',
                '#D4A574',
                1
            ))
            mazet_id = cursor.lastrowid

            # Créer la propriété Vaujany (Thème Bleu Montagne 🔵)
            cursor.execute('''
                INSERT INTO properties (name, slug, icon, location, description, theme, accent_color, display_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'Vaujany',
                'vaujany',
                '🏔️',
                'Vaujany, Isère',
                'Appartement à Vaujany',
                'vaujany',
                '#5B8FB9',
                2
            ))
            vaujany_id = cursor.lastrowid

            conn.commit()

            # Insérer les données par défaut pour Mazet BSA
            self._insert_mazet_data(cursor, mazet_id)

            # Insérer les données par défaut pour Vaujany
            self._insert_vaujany_data(cursor, vaujany_id)

            conn.commit()

    def _insert_mazet_data(self, cursor, property_id):
        """Insert default data for Mazet BSA"""

        # General Info
        cursor.execute('''
            INSERT INTO general_info (property_id, property_name, welcome_title, welcome_message, welcome_description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            property_id,
            'Le Mazet de BSA',
            'Bienvenue ! 🌿',
            'Nous sommes ravis de vous accueillir dans notre Mazet.',
            'Ce petit coin de paradis provençal est désormais le vôtre le temps de votre séjour.'
        ))

        # WiFi
        cursor.execute('''
            INSERT INTO wifi_config (property_id, ssid, password, location_description)
            VALUES (?, ?, ?, ?)
        ''', (
            property_id,
            'Roussel_Bonard_07',
            'Solex07700',
            'Le WiFi couvre l\'ensemble du mazet. La box se trouve dans le salon.'
        ))

        # Address
        cursor.execute('''
            INSERT INTO address (property_id, street, postal_code, city, country, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            '1 Chemin de sainte croix',
            '07700',
            'Bourg-Saint-Andéol',
            'France',
            'Le mazet se situe en plein cœur de Bourg-Saint-Andéol, à proximité immédiate des commerces et restaurants.'
        ))

        # Parking
        cursor.execute('''
            INSERT INTO parking_info (property_id, distance, description, is_free, tips)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            property_id,
            '150m',
            'Le parking le plus proche se trouve à environ 150 mètres du mazet. Tous les parkings de Bourg-Saint-Andéol sont gratuits.',
            1,
            'En été et les jours de marché (samedi), les places peuvent être plus difficiles à trouver près du centre.'
        ))

        # Access Info
        cursor.execute('''
            INSERT INTO access_info (property_id, check_in_time, check_out_time, keybox_code, keybox_location, access_instructions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            '16:00',
            '10:00',
            '1012',
            'La boîte à clés se trouve à l\'entrée principale.',
            'Utilisez ce code pour l\'ouvrir et récupérer les clés de la location.'
        ))

        # Contact Info
        cursor.execute('''
            INSERT INTO contact_info (property_id, host_name, phone, email, whatsapp, airbnb_url, description, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            'Votre hôte',
            '+33688461607',
            'solex07700@gmail.com',
            '33688461607',
            'https://www.airbnb.fr/rooms/1057934025843677755',
            'À votre service pour un séjour parfait en Ardèche',
            'Je réponds généralement dans l\'heure'
        ))

        # Emergency Numbers
        emergency_numbers = [
            (property_id, 'SAMU', '15', 'emergency', 1),
            (property_id, 'Pompiers', '18', 'emergency', 2),
            (property_id, 'Police', '17', 'emergency', 3),
            (property_id, 'Urgences Europe', '112', 'emergency', 4)
        ]
        cursor.executemany('''
            INSERT INTO emergency_numbers (property_id, name, number, category, display_order)
            VALUES (?, ?, ?, ?, ?)
        ''', emergency_numbers)

        # Activity Categories
        categories = [
            (property_id, 'Incontournables', 'star.fill', 'yellow', 1),
            (property_id, 'Baignade & Kayak', 'water.waves', 'blue', 2),
            (property_id, 'Villes à visiter', 'building.2.fill', 'purple', 3),
            (property_id, 'Nature & Randonnées', 'leaf.fill', 'green', 4),
            (property_id, 'Marchés provençaux', 'basket.fill', 'orange', 5)
        ]
        cursor.executemany('''
            INSERT INTO activity_categories (property_id, name, icon, color, display_order)
            VALUES (?, ?, ?, ?, ?)
        ''', categories)

        # Activities
        activities = [
            (property_id, 'Gorges de l\'Ardèche', 'Incontournables', 'Route panoramique spectaculaire', '🏞️', '15 min', 1),
            (property_id, 'Pont d\'Arc', 'Incontournables', 'Arche naturelle monumentale', '🌉', '20 min', 2),
            (property_id, 'Grotte Chauvet 2', 'Incontournables', 'Réplique de la grotte préhistorique', '🦴', '25 min', 3),
            (property_id, 'Ferme aux Crocodiles', 'Incontournables', 'Pierrelatte - Plus grand vivarium d\'Europe', '🐊', '15 min', 4),
            (property_id, 'Descente en canoë', 'Baignade & Kayak', 'Mini (8km) ou Maxi (32km)', '🛶', '25 min', 1),
            (property_id, 'Plages de l\'Ardèche', 'Baignade & Kayak', 'Saint-Martin-d\'Ardèche', '🏖️', '10 min', 2),
            (property_id, 'Montélimar', 'Villes à visiter', 'Capitale du nougat', '🍬', '25 min', 1),
            (property_id, 'Avignon', 'Villes à visiter', 'Palais des Papes', '🏰', '50 min', 2)
        ]
        cursor.executemany('''
            INSERT INTO activities (property_id, name, category, description, emoji, distance, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', activities)

        # Nearby Services
        services = [
            (property_id, 'Pharmacie du Rhône', 'pharmacy', '💊', 'Place du Champ de Mars, 07700 Bourg-Saint-Andéol', None, 'Pharmacie située en plein centre-ville', None, 1),
            (property_id, 'Intermarché SUPER', 'supermarket', '🛒', 'ZAC des Faysses, 07700 Bourg-Saint-Andéol', '0475544650', 'Supermarché complet', 'Lun-Sam: 8h30-19h30', 2),
            (property_id, 'Boulangerie Pâtisserie', 'bakery', '🥖', 'Place du Champ de Mars', None, 'Pain frais et pâtisseries', None, 3)
        ]
        cursor.executemany('''
            INSERT INTO nearby_services (property_id, name, category, icon, address, phone, description, opening_hours, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', services)

    def _insert_vaujany_data(self, cursor, property_id):
        """Insert default data for Vaujany"""

        # General Info
        cursor.execute('''
            INSERT INTO general_info (property_id, property_name, welcome_title, welcome_message, welcome_description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            property_id,
            'Appartement Vaujany',
            'Bienvenue ! 🏔️',
            'Bienvenue dans notre appartement au cœur des Alpes.',
            'Profitez de votre séjour à Vaujany, station familiale au pied de l\'Alpe d\'Huez.'
        ))

        # WiFi
        cursor.execute('''
            INSERT INTO wifi_config (property_id, ssid, password, location_description)
            VALUES (?, ?, ?, ?)
        ''', (
            property_id,
            'Vaujany_WiFi',
            'À configurer',
            'Le WiFi couvre l\'ensemble de l\'appartement.'
        ))

        # Address
        cursor.execute('''
            INSERT INTO address (property_id, street, postal_code, city, country, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            'À configurer',
            '38114',
            'Vaujany',
            'France',
            'L\'appartement se situe dans la station de Vaujany, au pied des pistes.'
        ))

        # Parking
        cursor.execute('''
            INSERT INTO parking_info (property_id, distance, description, is_free, tips)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            property_id,
            '50m',
            'Parking de la résidence disponible.',
            1,
            'En haute saison, pensez à arriver tôt pour avoir une place proche.'
        ))

        # Access Info
        cursor.execute('''
            INSERT INTO access_info (property_id, check_in_time, check_out_time, keybox_code, keybox_location, access_instructions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            '16:00',
            '10:00',
            'À configurer',
            'À configurer',
            'Instructions d\'accès à configurer.'
        ))

        # Contact Info
        cursor.execute('''
            INSERT INTO contact_info (property_id, host_name, phone, email, whatsapp, airbnb_url, description, response_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            'Votre hôte',
            '+33688461607',
            'solex07700@gmail.com',
            '33688461607',
            '',
            'À votre service pour un séjour parfait en montagne',
            'Je réponds généralement dans l\'heure'
        ))

        # Emergency Numbers
        emergency_numbers = [
            (property_id, 'SAMU', '15', 'emergency', 1),
            (property_id, 'Pompiers', '18', 'emergency', 2),
            (property_id, 'Police', '17', 'emergency', 3),
            (property_id, 'Urgences Europe', '112', 'emergency', 4),
            (property_id, 'Secours Montagne', '112', 'emergency', 5)
        ]
        cursor.executemany('''
            INSERT INTO emergency_numbers (property_id, name, number, category, display_order)
            VALUES (?, ?, ?, ?, ?)
        ''', emergency_numbers)

        # Activity Categories
        categories = [
            (property_id, 'Ski & Montagne', 'snowflake', 'blue', 1),
            (property_id, 'Randonnées', 'figure.hiking', 'green', 2),
            (property_id, 'Bien-être', 'sparkles', 'purple', 3),
            (property_id, 'Gastronomie', 'fork.knife', 'orange', 4)
        ]
        cursor.executemany('''
            INSERT INTO activity_categories (property_id, name, icon, color, display_order)
            VALUES (?, ?, ?, ?, ?)
        ''', categories)

        # Activities
        activities = [
            (property_id, 'Domaine Alpe d\'Huez', 'Ski & Montagne', '250km de pistes', '⛷️', '10 min', 1),
            (property_id, 'Télécabine Vaujany', 'Ski & Montagne', 'Accès direct aux pistes', '🚡', '2 min', 2),
            (property_id, 'Lac du Verney', 'Randonnées', 'Balade familiale', '🏞️', '15 min', 1),
            (property_id, 'Cascade de la Fare', 'Randonnées', 'Randonnée spectaculaire', '💧', '30 min', 2),
            (property_id, 'Centre aquatique', 'Bien-être', 'Piscine et spa', '🏊', '5 min', 1)
        ]
        cursor.executemany('''
            INSERT INTO activities (property_id, name, category, description, emoji, distance, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', activities)

        # Nearby Services
        services = [
            (property_id, 'Pharmacie de Vaujany', 'pharmacy', '💊', 'Centre village, 38114 Vaujany', None, 'Pharmacie du village', None, 1),
            (property_id, 'Sherpa Supermarché', 'supermarket', '🛒', 'Centre village, 38114 Vaujany', None, 'Épicerie de montagne', '8h-19h', 2),
            (property_id, 'Boulangerie Le Fournil', 'bakery', '🥖', 'Centre village', None, 'Pain frais et spécialités', None, 3)
        ]
        cursor.executemany('''
            INSERT INTO nearby_services (property_id, name, category, icon, address, phone, description, opening_hours, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', services)

    # ==================== Properties ====================

    def get_all_properties(self):
        conn = self.get_connection()
        results = conn.execute('SELECT * FROM properties WHERE is_active = 1 ORDER BY display_order').fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_property(self, property_id):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM properties WHERE id=?', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def get_property_by_slug(self, slug):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM properties WHERE slug=?', (slug,)).fetchone()
        conn.close()
        return dict(result) if result else None

    # ==================== General Info ====================

    def get_general_info(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM general_info WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_general_info(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE general_info
            SET property_name=?, welcome_title=?, welcome_message=?, welcome_description=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['property_name'], data['welcome_title'], data['welcome_message'], data['welcome_description'], property_id))
        conn.commit()
        conn.close()

    # ==================== WiFi ====================

    def get_wifi_config(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM wifi_config WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_wifi_config(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE wifi_config
            SET ssid=?, password=?, location_description=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['ssid'], data['password'], data['location_description'], property_id))
        conn.commit()
        conn.close()

    # ==================== Address ====================

    def get_address(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM address WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_address(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE address
            SET street=?, postal_code=?, city=?, country=?, description=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['street'], data['postal_code'], data['city'], data['country'], data['description'], property_id))
        conn.commit()
        conn.close()

    # ==================== Parking ====================

    def get_parking_info(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM parking_info WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_parking_info(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE parking_info
            SET distance=?, description=?, is_free=?, tips=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['distance'], data['description'], data.get('is_free', True), data.get('tips', ''), property_id))
        conn.commit()
        conn.close()

    # ==================== Access ====================

    def get_access_info(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM access_info WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_access_info(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE access_info
            SET check_in_time=?, check_out_time=?, keybox_code=?, keybox_location=?, access_instructions=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['check_in_time'], data['check_out_time'], data['keybox_code'], data['keybox_location'], data['access_instructions'], property_id))
        conn.commit()
        conn.close()

    # ==================== Contact ====================

    def get_contact_info(self, property_id=1):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM contact_info WHERE property_id=? ORDER BY id DESC LIMIT 1', (property_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def update_contact_info(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contact_info
            SET host_name=?, phone=?, email=?, whatsapp=?, airbnb_url=?, description=?, response_time=?, updated_at=CURRENT_TIMESTAMP
            WHERE property_id=?
        ''', (data['host_name'], data['phone'], data['email'], data.get('whatsapp', ''), data.get('airbnb_url', ''), data.get('description', ''), data.get('response_time', ''), property_id))
        conn.commit()
        conn.close()

    # ==================== Activities ====================

    def get_all_activities(self, property_id=1):
        conn = self.get_connection()
        results = conn.execute('SELECT * FROM activities WHERE property_id=? ORDER BY category, display_order', (property_id,)).fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_activity(self, activity_id):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM activities WHERE id=?', (activity_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def create_activity(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activities (property_id, name, category, description, emoji, distance, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (property_id, data['name'], data['category'], data['description'], data['emoji'], data['distance'], data.get('display_order', 0)))
        conn.commit()
        activity_id = cursor.lastrowid
        conn.close()
        return activity_id

    def update_activity(self, activity_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE activities
            SET name=?, category=?, description=?, emoji=?, distance=?, display_order=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (data['name'], data['category'], data['description'], data['emoji'], data['distance'], data.get('display_order', 0), activity_id))
        conn.commit()
        conn.close()

    def delete_activity(self, activity_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM activities WHERE id=?', (activity_id,))
        conn.commit()
        conn.close()

    # ==================== Emergency ====================

    def get_all_emergency_numbers(self, property_id=1):
        conn = self.get_connection()
        results = conn.execute('SELECT * FROM emergency_numbers WHERE property_id=? ORDER BY display_order', (property_id,)).fetchall()
        conn.close()
        return [dict(row) for row in results]

    # ==================== Services ====================

    def get_all_nearby_services(self, property_id=1):
        conn = self.get_connection()
        results = conn.execute('SELECT * FROM nearby_services WHERE property_id=? ORDER BY display_order', (property_id,)).fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_nearby_service(self, service_id):
        conn = self.get_connection()
        result = conn.execute('SELECT * FROM nearby_services WHERE id=?', (service_id,)).fetchone()
        conn.close()
        return dict(result) if result else None

    def create_nearby_service(self, property_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nearby_services (property_id, name, category, icon, address, phone, description, opening_hours, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (property_id, data['name'], data['category'], data.get('icon'), data['address'], data.get('phone'), data.get('description'), data.get('opening_hours'), data.get('display_order', 0)))
        conn.commit()
        service_id = cursor.lastrowid
        conn.close()
        return service_id

    def update_nearby_service(self, service_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE nearby_services
            SET name=?, category=?, icon=?, address=?, phone=?, description=?, opening_hours=?, display_order=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (data['name'], data['category'], data.get('icon'), data['address'], data.get('phone'), data.get('description'), data.get('opening_hours'), data.get('display_order', 0), service_id))
        conn.commit()
        conn.close()

    def delete_nearby_service(self, service_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM nearby_services WHERE id=?', (service_id,))
        conn.commit()
        conn.close()

    # ==================== Activity Categories ====================

    def get_all_activity_categories(self, property_id=1):
        conn = self.get_connection()
        results = conn.execute('SELECT * FROM activity_categories WHERE property_id=? ORDER BY display_order', (property_id,)).fetchall()
        conn.close()
        return [dict(row) for row in results]

    # ==================== Export ====================

    def export_all_data(self, property_id=1):
        """Export all data as JSON for the iOS app"""
        data = {
            'general_info': self.get_general_info(property_id),
            'wifi': self.get_wifi_config(property_id),
            'address': self.get_address(property_id),
            'parking': self.get_parking_info(property_id),
            'access': self.get_access_info(property_id),
            'contact': self.get_contact_info(property_id),
            'emergency_numbers': self.get_all_emergency_numbers(property_id),
            'nearby_services': self.get_all_nearby_services(property_id),
            'activities': self.get_all_activities(property_id),
            'activity_categories': self.get_all_activity_categories(property_id),
            'exported_at': datetime.now().isoformat()
        }
        return data
