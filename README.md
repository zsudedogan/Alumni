 🎓 Alumni — Alumni Tracking & Networking Platform

**Alumni** is a web application that helps graduates stay connected with each other and with their institution. It provides core features such as profile management, an alumni directory, events, and communication tools. The project is built using **Node.js**, **JavaScript**, and **MySQL**.

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Folder Structure](#-folder-structure)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Setup](#step-by-step-setup)
  - [Environment Variables (.env)](#environment-variables-env)
  - [Database Setup](#database-setup)
- [Usage](#-usage)
- [Sample Database Schema](#-sample-database-schema)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [FAQ](#-faq)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 About the Project

The Alumni project was built to strengthen the digital connection between educational institutions (or communities) and their graduates. Users can register, build a profile, search for other alumni, stay updated on events, and administrators can manage alumni data through a dedicated admin panel.

Alumni is a full-stack application powered by a **Node.js**-based server, a **MySQL** database, and **JavaScript** on the client side (optionally paired with a frontend framework).

> 💡 This README is a comprehensive guide describing the project's overall structure and setup process. It's recommended to keep this file updated as the project evolves.

---

## ✨ Features

- 👤 **User Registration & Login** — Secure authentication for alumni accounts
- 🔐 **Role-Based Authorization** — Admin, moderator, and standard alumni roles
- 🗂️ **Alumni Profiles** — Store graduation year, department, contact info, profession, and location
- 🔎 **Advanced Search & Filtering** — Search alumni by department, year, city, or industry
- 📅 **Event Management** — Announce alumni gatherings and events, and track attendance
- 💬 **Messaging** — Infrastructure for communication between alumni
- 📊 **Admin Dashboard** — Alumni statistics, pending approvals, and general management screen
- 🔔 **Notification System** — Notify users about new events or announcements
- 🌐 **RESTful API** — JSON-based communication between frontend and backend
- 📱 **Responsive Design** — Mobile- and desktop-friendly interface

> Note: The feature list above reflects the project's intended scope; some items may not yet be implemented depending on development progress.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Node.js, Express.js |
| **Database** | MySQL |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla or chosen framework) |
| **Authentication** | JWT (JSON Web Token) / bcrypt |
| **ORM / Query Builder** | mysql2 / Sequelize (optional) |
| **Environment Management** | dotenv |
| **API Testing** | Postman / Insomnia |
| **Version Control** | Git & GitHub |

---

## 🏗️ System Architecture

```
┌────────────────┐        HTTP Requests          ┌────────────────────┐
│                │ ───────────────────────────▶ │                    │
│    Client      │                               │   Node.js Server   │
│ (Browser/JS)   │ ◀─────────────────────────── │   (Express API)    │
│                │        JSON Responses         │                    │
└────────────────┘                               └─────────┬──────────┘
                                                             │
                                                       SQL Queries
                                                             │
                                                             ▼
                                                   ┌────────────────────┐
                                                   │   MySQL Database   │
                                                   └────────────────────┘
```

The application follows a classic **MVC (Model-View-Controller)** architecture composed of three layers: the client, the application server (API), and the database.

---

## 📁 Folder Structure

The structure below shows the recommended directory organization for the project:

```
Alumni/
├── config/
│   └── db.js                # Database connection settings
├── controllers/
│   ├── authController.js    # Register/login logic
│   ├── userController.js    # User/alumni operations
│   └── eventController.js   # Event operations
├── models/
│   ├── userModel.js
│   └── eventModel.js
├── routes/
│   ├── authRoutes.js
│   ├── userRoutes.js
│   └── eventRoutes.js
├── middlewares/
│   ├── authMiddleware.js     # JWT verification
│   └── errorHandler.js
├── public/
│   ├── css/
│   ├── js/
│   └── images/
├── views/                    # (If server-side templates are used)
├── database/
│   └── alumni.sql            # Database schema / seed file
├── .env.example
├── .gitignore
├── package.json
├── server.js                 # Application entry point
└── README.md
```

> This layout is a suggestion — feel free to adapt folder names to fit your own project structure.

---

## ⚙️ Installation

### Prerequisites

Before running the project, make sure the following are installed on your machine:

- [Node.js](https://nodejs.org/) (v16 or higher recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js) or [yarn](https://yarnpkg.com/)
- [MySQL](https://www.mysql.com/) (v5.7 or higher) or [MariaDB](https://mariadb.org/)
- [Git](https://git-scm.com/)

### Step-by-Step Setup

**1. Clone the repository**

```bash
git clone https://github.com/zsudedogan/Alumni.git
cd Alumni
```

**2. Install dependencies**

```bash
npm install
```

**3. Create your `.env` file**

Copy `.env.example` in the project root to create your own `.env` file:

```bash
cp .env.example .env
```

**4. Set up your database and edit the `.env` file** (see the relevant sections below)

**5. Start the application**

```bash
npm start
```

To run in development mode (with automatic restarts), you can use `nodemon`:

```bash
npm run dev
```

By default, the application will run at:

```
http://localhost:3000
```

---

### Environment Variables (`.env`)

Example of environment variables the project needs:

```env
# Server Settings
PORT=3000
NODE_ENV=development

# Database Settings
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=alumni_db

# JWT / Authentication
JWT_SECRET=your_super_secret_key
JWT_EXPIRES_IN=7d

# Other
CLIENT_URL=http://localhost:3000
```

> ⚠️ Never commit your `.env` file to GitHub. Make sure `.env` is listed in your `.gitignore` file.

---

### Database Setup

**1.** Connect to your MySQL server:

```bash
mysql -u root -p
```

**2.** Create the database:

```sql
CREATE DATABASE alumni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**3.** If you have a ready-made schema file, import it:

```bash
mysql -u root -p alumni_db < database/alumni.sql
```

**4.** Make sure the database credentials in your `.env` file (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) are correct.

---

## ▶️ Usage

Once the installation is complete:

1. Start the server: `npm start` or `npm run dev`
2. Open your browser and go to `http://localhost:3000`
3. Create a new alumni account or log in with an existing one
4. Complete your profile, browse other alumni, and check out events

When logged in as an admin, you'll have access to a management dashboard where you can approve, edit, or delete alumni records.

---

## 🗄️ Sample Database Schema

Below is a sample table structure that can serve as a foundation for the project:

```sql
-- Users / Alumni Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    graduation_year YEAR NOT NULL,
    department VARCHAR(100),
    profession VARCHAR(100),
    city VARCHAR(100),
    phone VARCHAR(20),
    profile_photo VARCHAR(255),
    role ENUM('admin', 'alumni') DEFAULT 'alumni',
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Events Table
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATETIME NOT NULL,
    location VARCHAR(200),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Event Participants Table
CREATE TABLE event_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Messages Table
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);
```

> This schema is for illustration purposes only — feel free to add or remove fields based on your project's actual needs.

---

## 🔌 API Endpoints

Below are sample endpoints typically found in an Alumni API:

### 🔐 Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Registers a new alumni account |
| `POST` | `/api/auth/login` | Logs a user in and returns a token |
| `POST` | `/api/auth/logout` | Ends the user's session |

### 👤 Users / Alumni

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/users` | Lists all alumni |
| `GET` | `/api/users/:id` | Retrieves a specific alumni's info |
| `PUT` | `/api/users/:id` | Updates alumni information |
| `DELETE` | `/api/users/:id` | Deletes an alumni record *(admin only)* |
| `GET` | `/api/users/search?department=&year=&city=` | Filtered alumni search |

### 📅 Events

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/events` | Lists all events |
| `POST` | `/api/events` | Creates a new event *(admin/authorized)* |
| `PUT` | `/api/events/:id` | Updates event details |
| `DELETE` | `/api/events/:id` | Deletes an event |
| `POST` | `/api/events/:id/join` | Registers the user's attendance for an event |

### 💬 Messaging

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/messages/:userId` | Retrieves message history with a specific user |
| `POST` | `/api/messages` | Sends a new message |

> Note: Endpoints may vary depending on your actual route definitions — this table is a general reference.

---

## 🧪 Testing

You can use tools like [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/) to test the API endpoints.

```bash
# Example: login request
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"example@mail.com","password":"password123"}'
```

For automated testing, libraries such as `Jest` or `Mocha/Chai` can be integrated:

```bash
npm run test
```

---

## 🗺️ Roadmap

- [ ] User registration & login system
- [ ] Alumni profile pages
- [ ] Search and filtering
- [ ] Event management module
- [ ] Messaging system
- [ ] Notification infrastructure
- [ ] Admin dashboard
- [ ] Email verification
- [ ] Social login (Google/LinkedIn sign-in)
- [ ] Mobile app support

---

## 🤝 Contributing

If you'd like to contribute to this project:

1. **Fork** this repository
2. Create a new feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m "Add: new feature ..."`)
4. Push your branch (`git push origin feature/new-feature`)
5. Open a **Pull Request**

Please try to follow the existing code style and write descriptive commit messages before contributing.

---

## ❓ FAQ

**Q: I'm getting an `Error: connect ECONNREFUSED` error, what should I do?**
Make sure your MySQL service is running and that the `DB_HOST` and `DB_PORT` values in your `.env` file are correct.

**Q: I'm getting an error during `npm install`.**
Make sure your Node.js version is up to date, then try deleting the `node_modules` folder and running `npm install` again.

**Q: I'm getting a token verification error.**
Make sure `JWT_SECRET` is correctly defined in your `.env` file, and that you're sending the `Authorization: Bearer <token>` header with your requests.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for more details.

---

## 📬 Contact

For questions, suggestions, or contributions:

- **GitHub:** [zsudedogan/Alumni](https://github.com/zsudedogan/Alumni)
- **Issues:** Use the [Issues](https://github.com/zsudedogan/Alumni/issues) tab to report bugs or suggest features.
