package com.example.taskmanager.controller;

import com.example.taskmanager.model.Task;
import com.example.taskmanager.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@Controller
public class TaskController {
    
    @Autowired
    private TaskService taskService;
    
    // Web endpoints
    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("tasks", taskService.getAllTasks());
        model.addAttribute("newTask", new Task());
        return "index";
    }
    
    @PostMapping("/tasks")
    public String createTask(@ModelAttribute Task task) {
        taskService.createTask(task.getTitle(), task.getDescription());
        return "redirect:/";
    }
    
    @PostMapping("/tasks/{id}/toggle")
    public String toggleTask(@PathVariable Long id) {
        taskService.toggleTaskCompletion(id);
        return "redirect:/";
    }
    
    @PostMapping("/tasks/{id}/delete")
    public String deleteTask(@PathVariable Long id) {
        taskService.deleteTask(id);
        return "redirect:/";
    }
    
    // REST API endpoints
    @GetMapping("/api/tasks")
    @ResponseBody
    public List<Task> getAllTasksApi() {
        return taskService.getAllTasks();
    }
    
    @GetMapping("/api/tasks/{id}")
    @ResponseBody
    public ResponseEntity<Task> getTaskApi(@PathVariable Long id) {
        Optional<Task> task = taskService.getTaskById(id);
        return task.map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping("/api/tasks")
    @ResponseBody
    public Task createTaskApi(@RequestBody Task task) {
        return taskService.createTask(task.getTitle(), task.getDescription());
    }
    
    @PutMapping("/api/tasks/{id}")
    @ResponseBody
    public ResponseEntity<Task> updateTaskApi(@PathVariable Long id, @RequestBody Task task) {
        Task updatedTask = taskService.updateTask(id, task.getTitle(), task.getDescription());
        return updatedTask != null ? ResponseEntity.ok(updatedTask) : ResponseEntity.notFound().build();
    }
    
    @PutMapping("/api/tasks/{id}/toggle")
    @ResponseBody
    public ResponseEntity<Task> toggleTaskApi(@PathVariable Long id) {
        Task toggledTask = taskService.toggleTaskCompletion(id);
        return toggledTask != null ? ResponseEntity.ok(toggledTask) : ResponseEntity.notFound().build();
    }
    
    @DeleteMapping("/api/tasks/{id}")
    @ResponseBody
    public ResponseEntity<Void> deleteTaskApi(@PathVariable Long id) {
        boolean deleted = taskService.deleteTask(id);
        return deleted ? ResponseEntity.ok().build() : ResponseEntity.notFound().build();
    }
    
    @GetMapping("/api/tasks/search")
    @ResponseBody
    public List<Task> searchTasksApi(@RequestParam String q) {
        return taskService.searchTasks(q);
    }
    
}