# Task Manager Web Application

A modern, responsive task management web application built with Spring Boot and Thymeleaf.

## Features

- ✅ Create, read, update, and delete tasks
- ✅ Mark tasks as completed or pending
- ✅ Beautiful and responsive UI
- ✅ RESTful API endpoints
- ✅ In-memory H2 database
- ✅ Modern design with animations and hover effects

## Technologies Used

- **Backend**: Spring Boot 3.2.0, Spring Data JPA, Spring Web
- **Frontend**: Thymeleaf, HTML5, CSS3, JavaScript
- **Database**: H2 (in-memory)
- **Build Tool**: Maven
- **Java Version**: 17+

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

## How to Run

1. **Clone or navigate to the project directory**
   ```bash
   cd /workspace
   ```

2. **Build the application**
   ```bash
   mvn clean compile
   ```

3. **Run the application**
   ```bash
   mvn spring-boot:run
   ```

4. **Access the application**
   - Open your web browser and go to: `http://localhost:8080`
   - The application will start with an empty task list

## API Endpoints

### Web Interface
- `GET /` - Main task management interface

### REST API
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/{id}` - Get a specific task
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `PUT /api/tasks/{id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete a task
- `GET /api/tasks/search?q={query}` - Search tasks by title

### Development Tools
- `http://localhost:8080/h2-console` - H2 Database Console
  - JDBC URL: `jdbc:h2:mem:taskdb`
  - Username: `sa`
  - Password: (leave empty)

## Project Structure

```
src/
├── main/
│   ├── java/com/example/taskmanager/
│   │   ├── TaskManagerApplication.java     # Main application class
│   │   ├── controller/
│   │   │   └── TaskController.java         # Web and REST controllers
│   │   ├── model/
│   │   │   └── Task.java                   # Task entity
│   │   ├── repository/
│   │   │   └── TaskRepository.java         # Data access layer
│   │   └── service/
│   │       └── TaskService.java            # Business logic
│   └── resources/
│       ├── application.properties          # Application configuration
│       ├── static/css/
│       │   └── style.css                   # CSS styling
│       └── templates/
│           └── index.html                  # Main HTML template
└── pom.xml                                 # Maven configuration
```

## Usage

1. **Adding Tasks**: Use the form at the top to add new tasks with a title and optional description.

2. **Managing Tasks**: Each task card provides buttons to:
   - ✅ Toggle completion status
   - 🗑️ Delete the task

3. **Task Status**: Tasks are visually distinguished:
   - Pending tasks have a blue left border
   - Completed tasks have a green left border and are slightly dimmed

## Sample API Usage

### Create a task
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Spring Boot", "description": "Complete the Spring Boot tutorial"}'
```

### Get all tasks
```bash
curl http://localhost:8080/api/tasks
```

### Toggle task completion
```bash
curl -X PUT http://localhost:8080/api/tasks/1/toggle
```

## Development Notes

- The application uses an in-memory H2 database, so data is reset on each restart
- Hot reloading is enabled with Spring Boot DevTools
- The UI is fully responsive and works on mobile devices
- CSS includes modern animations and hover effects for better UX

## Building for Production

To build a production-ready JAR file:

```bash
mvn clean package
java -jar target/task-manager-1.0.0.jar
```

---

**Enjoy managing your tasks!** 🎯