package com.example.taskmanager.service;

import com.example.taskmanager.model.Task;
import com.example.taskmanager.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class TaskService {
    
    @Autowired
    private TaskRepository taskRepository;
    
    public List<Task> getAllTasks() {
        return taskRepository.findAllByOrderByCreatedAtDesc();
    }
    
    public List<Task> getCompletedTasks() {
        return taskRepository.findByCompletedOrderByCreatedAtDesc(true);
    }
    
    public List<Task> getPendingTasks() {
        return taskRepository.findByCompletedOrderByCreatedAtDesc(false);
    }
    
    public Optional<Task> getTaskById(Long id) {
        return taskRepository.findById(id);
    }
    
    public Task saveTask(Task task) {
        return taskRepository.save(task);
    }
    
    public Task createTask(String title, String description) {
        Task task = new Task(title, description);
        return taskRepository.save(task);
    }
    
    public Task updateTask(Long id, String title, String description) {
        Optional<Task> taskOptional = taskRepository.findById(id);
        if (taskOptional.isPresent()) {
            Task task = taskOptional.get();
            task.setTitle(title);
            task.setDescription(description);
            return taskRepository.save(task);
        }
        return null;
    }
    
    public Task toggleTaskCompletion(Long id) {
        Optional<Task> taskOptional = taskRepository.findById(id);
        if (taskOptional.isPresent()) {
            Task task = taskOptional.get();
            task.setCompleted(!task.isCompleted());
            return taskRepository.save(task);
        }
        return null;
    }
    
    public boolean deleteTask(Long id) {
        if (taskRepository.existsById(id)) {
            taskRepository.deleteById(id);
            return true;
        }
        return false;
    }
    
    public List<Task> searchTasks(String query) {
        return taskRepository.findByTitleContainingIgnoreCaseOrderByCreatedAtDesc(query);
    }
    
}