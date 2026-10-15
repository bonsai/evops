#!/usr/bin/env node
/**
 * TUI for Kanban Management (kanban PM)
 * 
 * Features:
 * - List all kanban tasks
 * - Add new task
 * - Edit task details
 * - Delete task
 * - Save to kanban.json
 * 
 * Usage:
 *   node tui.js list
 *   node tui.js add "Task title" "Description"
 *   node tui.js edit 1 "New title" "New description"
 *   node tui.js delete 1
 * 
 * The kanban data is stored in kanban.json in the current working directory.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Path to kanban data file (kanban.json in current directory)
const KANBAN_FILE = path.join(process.cwd(), 'kanban.json');

// Helper: Load kanban data
function loadKanban() {
  try {
    const data = fs.readFileSync(KANBAN_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    // If file doesn't exist, return empty array
    return [];
  }
}

// Helper: Save kanban data
function saveKanban(data) {
  fs.writeFileSync(KANBAN_FILE, JSON.stringify(data, null, 2));
}

// Display the kanban list
function showList(tasks) {
  console.log('\n=== Kanban Tasks ===');
  if (tasks.length === 0) {
    console.log('No tasks found.');
    return;
  }
  
  tasks.forEach((task, index) => {
    console.log(`${index + 1}. [${task.status}] ${task.title}`);
  }
}

// Prompt helper
function ask(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  return new Promise(resolve => rl.question(question, answer => {
    rl.close();
    resolve(answer);
  });
}

// Main TUI function
async function showTUI() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  while (true) {
    const tasks = loadKanban();
    showList(tasks);
    
    const action = await ask('Choose action (list, add, edit, delete, quit): ');
    
    if (action.toLowerCase() === 'list') {
      showList(tasks);
    } else if (action.toLowerCase() === 'add') {
      const title = await ask('Enter task title: ');
      const description = await ask('Enter task description: ');
      const newTask = {
        id: Date.now(),
        title,
        description,
        status: 'todo',
        createdAt: new Date().toISOString()
      };
      tasks.push(newTask);
      saveKanban(tasks);
      console.log('Task added successfully!');
    } else if (action.toLowerCase() === 'edit') {
      const index = await ask('Enter task number to edit: ');
      const indexNum = parseInt(index, 10) - 1;
      if (indexNum >= 0 && indexNum < tasks.length) {
        const task = tasks[indexNum];
        const newTitle = await ask('Enter new title: ');
        const newDesc = await ask('Enter new description: ');
        task.title = newTitle;
        task.description = newDesc;
        saveKanban(tasks);
        console.log('Task updated!');
      } else {
        console.log('Invalid task number');
      }
    } else if (action.toLowerCase() === 'delete') {
      const index = await ask('Enter task number to delete: ');
      const indexNum = parseInt(index, 10) - 1;
      if (indexNum >= 0 && indexNum < tasks.length) {
        tasks.splice(indexNum, 1);
        saveKanban(tasks);
        console.log('Task deleted');
      } else {
        console.log('Invalid task number');
      }
    } else if (action.toLowerCase() === 'quit') {
      console.log('Exiting TUI...');
      rl.close();
      process.exit(0);
    } else {
      console.log('Invalid action. Use: list, add, edit, delete, quit');
    }
  }
}

// Start the TUI
showTUI();