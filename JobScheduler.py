import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling")
        self.root.geometry("1130x600")
        self.Gui()

    def Gui(self):
        # Input Frame
        self.input_frame = tk.Frame(self.root, padx=10, pady=20)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        tk.Label(self.input_frame, text="Input", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

        # Algorithm Dropdown
        tk.Label(self.input_frame, text="Algorithm", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=(10, 2))
        self.algorithm_var = tk.StringVar(value="First Come First Serve, FCFS")
        algorithms = [
            "First Come First Serve, FCFS",
            "Shortest Job First, SJF",
            "Shortest Remaining Time First, SRTF",
            "Priority Scheduling (Preemptive)",
            "Priority Scheduling (Non-Preemptive)",
            "Round Robin, RR",
        ]
        self.algorithm_dropdown = ttk.Combobox(self.input_frame, textvariable=self.algorithm_var, values=algorithms)
        self.algorithm_dropdown.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)
        self.algorithm_dropdown.bind("<<ComboboxSelected>>", self.update_table_columns)

        # Number of Processes Section
        tk.Label(self.input_frame, text="Number of Processes:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5)
        self.num_processes_var = tk.IntVar()
        tk.Entry(self.input_frame, textvariable=self.num_processes_var).grid(row=2, column=1, padx=5, sticky="ew")
        tk.Button(self.input_frame, text="Set", command=self.set_process_inputs).grid(row=2, column=2, padx=5)

        # Process Input Frame
        self.process_input_frame = tk.Frame(self.input_frame)
        self.process_input_frame.grid(row=3, column=0, columnspan=3, sticky="w", pady=10)

        self.include_priority_column = False
        self.include_quantum_time = False

        # Solve Button
        self.solve_button = tk.Button(self.input_frame, text="Solve", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.solve)
        self.solve_button.grid(row=5, column=0, columnspan=3, pady=20)

        # Output Frame
        output_frame = tk.Frame(self.root, padx=5, pady=20)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(output_frame, text="Output", font=("Arial", 16, "bold")).pack(anchor="w")

        self.output_text = tk.Text(output_frame, height=20, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def update_table_columns(self, event=None):
        selected_algorithm = self.algorithm_var.get()
        self.include_priority_column = selected_algorithm in [
            "Priority Scheduling (Preemptive)",
            "Priority Scheduling (Non-Preemptive)",
        ]

        if hasattr(self, "quantum_label"):
            self.quantum_label.destroy()
        if hasattr(self, "quantum_entry"):
            self.quantum_entry.destroy()

        if selected_algorithm == "Round Robin, RR":
            self.include_quantum_time = True
            self.quantum_label = tk.Label(self.input_frame, text="Quantum Time:")
            self.quantum_label.grid(row=4, column=0, sticky="w", padx=5)

            self.quantum_var = tk.IntVar()
            self.quantum_entry = tk.Entry(self.input_frame, textvariable=self.quantum_var)
            self.quantum_entry.grid(row=4, column=1, padx=5, sticky="ew")
        else:
            self.include_quantum_time = False

        self.set_process_inputs()

    def set_process_inputs(self):
        try:
            n = self.num_processes_var.get()
            if n <= 0:
                raise ValueError("Number of processes must be greater than zero.")

            for widget in self.process_input_frame.winfo_children():
                widget.destroy()

            tk.Label(self.process_input_frame, text="Process Name").grid(row=0, column=0, padx=5)
            tk.Label(self.process_input_frame, text="Arrival Time").grid(row=0, column=1, padx=5)
            tk.Label(self.process_input_frame, text="Burst Time").grid(row=0, column=2, padx=5)

            if self.include_priority_column:
                tk.Label(self.process_input_frame, text="Priority").grid(row=0, column=3, padx=5)

            self.process_inputs = []
            for i in range(n):
                process_name = tk.Entry(self.process_input_frame)
                arrival_time = tk.Entry(self.process_input_frame)
                burst_time = tk.Entry(self.process_input_frame)

                process_name.grid(row=i + 1, column=0, padx=5, pady=2)
                arrival_time.grid(row=i + 1, column=1, padx=5, pady=2)
                burst_time.grid(row=i + 1, column=2, padx=5, pady=2)

                if self.include_priority_column:
                    priority = tk.Entry(self.process_input_frame)
                    priority.grid(row=i + 1, column=3, padx=5, pady=2)
                    self.process_inputs.append((process_name, arrival_time, burst_time, priority))
                else:
                    self.process_inputs.append((process_name, arrival_time, burst_time))

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def solve(self):
        try:
            algorithm = self.algorithm_var.get()
            process_names = []
            arrival_times = []
            burst_times = []
            priorities = []

            for inputs in self.process_inputs:
                process_name = inputs[0].get().strip()
                if not process_name:
                    raise ValueError("Process names cannot be empty.")
                process_names.append(process_name)

                arrival_time = int(inputs[1].get())
                burst_time = int(inputs[2].get())
                arrival_times.append(arrival_time)
                burst_times.append(burst_time)

                if self.include_priority_column:
                    priority = int(inputs[3].get())
                    priorities.append(priority)

            if self.include_quantum_time:
                quantum_time = int(self.quantum_var.get())

            if algorithm == "First Come First Serve, FCFS":
                self.fcfs(process_names, arrival_times, burst_times)
            elif algorithm == "Shortest Job First, SJF":
                self.sjf(process_names, arrival_times, burst_times)
            elif algorithm=="Shortest Remaining Time First, SRTF":
                self.srtf(process_names, arrival_times, burst_times)
            elif algorithm == "Priority Scheduling (Preemptive)":
                self.priority_preemptive(process_names, arrival_times, burst_times, priorities)  
            elif algorithm=="Priority Scheduling (Non-Preemptive)":
                self.priority_non_preemptive(process_names, arrival_times, burst_times, priorities) 
            elif algorithm=="Round Robin, RR":
                self.round_robin(process_names, arrival_times, burst_times, quantum_time)     
        except ValueError as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {e}")

    def fcfs(self, process_names, arrival_times, burst_times):
        processes = sorted(zip(process_names, arrival_times, burst_times), key=lambda x: x[1])  # Sort by arrival time
        gantt_chart = []
        time = 0

        # Initialize metrics
        turnaround_times = []
        waiting_times = []

        for process_name, arrival_time, burst_time in processes:
            if time < arrival_time:
                time = arrival_time  # Wait until the process arrives
            start_time = time
            time += burst_time
            end_time = time

            # Calculate turnaround and waiting times
            turnaround_time = end_time - arrival_time
            waiting_time = turnaround_time - burst_time

            turnaround_times.append(turnaround_time)
            waiting_times.append(waiting_time)

            gantt_chart.append((process_name, start_time, end_time))

        # Calculate averages
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
        avg_waiting_time = sum(waiting_times) / len(waiting_times)

        # Display Gantt chart and results
        self.plot_gantt_chart(gantt_chart, "FCFS Scheduling")
        self.display_results(processes, turnaround_times, waiting_times, avg_turnaround_time, avg_waiting_time)

    def sjf(self, process_names, arrival_times, burst_times):
        processes = sorted(zip(process_names, arrival_times, burst_times), key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
        gantt_chart = []
        time = 0
        completed = []

        # Initialize metrics
        turnaround_times = []
        waiting_times = []

        while len(completed) < len(processes):
            available_processes = [p for p in processes if p[1] <= time and p not in completed]
            if available_processes:
                current_process = min(available_processes, key=lambda x: x[2])  # Select process with shortest burst time
                process_name, arrival_time, burst_time = current_process
                start_time = time
                time += burst_time
                end_time = time

                # Calculate turnaround and waiting times
                turnaround_time = end_time - arrival_time
                waiting_time = turnaround_time - burst_time

                turnaround_times.append(turnaround_time)
                waiting_times.append(waiting_time)

                gantt_chart.append((process_name, start_time, end_time))
                completed.append(current_process)
            else:
                time += 1  # Increment time if no process is available

        # Calculate averages
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
        avg_waiting_time = sum(waiting_times) / len(waiting_times)

        # Display Gantt chart and results
        self.plot_gantt_chart(gantt_chart, "SJF Scheduling")
        self.display_results(processes, turnaround_times, waiting_times, avg_turnaround_time, avg_waiting_time)

    def srtf(self, process_names, arrival_times, burst_times):

        processes = list(zip(process_names, arrival_times, burst_times))
        n = len(processes)
        remaining_times = {name: burst for name, _, burst in processes}
        completed = 0
        time = 0
        gantt_chart = []
        turnaround_times = {name: 0 for name in process_names}
        waiting_times = {name: 0 for name in process_names}
        while completed < n:
            available = [(name, remaining_times[name]) for name, arrival, _ in processes if arrival <= time and remaining_times[name] > 0]
            if available:
                available.sort(key=lambda x: x[1])  # Sort by remaining time
                current_process = available[0][0]

                gantt_chart.append((current_process, time, time + 1))  # Process runs for 1 unit time
                remaining_times[current_process] -= 1
                time += 1

                if remaining_times[current_process] == 0:
                    completed += 1
                    end_time = time
                    arrival_time = next(arrival for name, arrival, _ in processes if name == current_process)
                    burst_time = next(burst for name, _, burst in processes if name == current_process)

                    turnaround_times[current_process] = end_time - arrival_time
                    waiting_times[current_process] = turnaround_times[current_process] - burst_time
            else:
                time += 1  # Idle time

        # Calculate averages
        avg_turnaround_time = sum(turnaround_times.values()) / n
        avg_waiting_time = sum(waiting_times.values()) / n

        # Consolidate Gantt chart
        consolidated_gantt = []
        for name, start, end in gantt_chart:
            if consolidated_gantt and consolidated_gantt[-1][0] == name:
                consolidated_gantt[-1] = (name, consolidated_gantt[-1][1], end)
            else:
                consolidated_gantt.append((name, start, end))

        # Display Gantt chart and results
        self.plot_gantt_chart(consolidated_gantt, "SRTF Scheduling")
        self.display_results([(name, arrival, burst) for name, arrival, burst in processes],list(turnaround_times.values()),list(waiting_times.values()), avg_turnaround_time, avg_waiting_time)        
    
    def priority_preemptive(self, process_names, arrival_times, burst_times, priorities):
     processes = list(zip(process_names, arrival_times, burst_times, priorities))
     remaining_times = {p[0]: p[2] for p in processes}  # Remaining burst times
     gantt_chart = []
     time = 0
     completed = 0
     n = len(processes)

     # Initialize metrics
     turnaround_times = {p[0]: 0 for p in processes}
     waiting_times = {p[0]: 0 for p in processes}
     end_times = {}

     while completed < n:
        available_processes = [p for p in processes if p[1] <= time and remaining_times[p[0]] > 0]
        if not available_processes:
            time += 1
            continue

        highest_priority_process = min(available_processes, key=lambda x: (x[3], x[1]))
        process_name, arrival_time, _, _ = highest_priority_process

        if gantt_chart and gantt_chart[-1][0] == process_name:
            gantt_chart[-1] = (process_name, gantt_chart[-1][1], time + 1)
        else:
            gantt_chart.append((process_name, time, time + 1))

        remaining_times[process_name] -= 1
        time += 1

        if remaining_times[process_name] == 0:
            completed += 1
            end_times[process_name] = time
            turnaround_times[process_name] = end_times[process_name] - arrival_time
            waiting_times[process_name] = turnaround_times[process_name] - burst_times[process_names.index(process_name)]

     # Calculate averages
     avg_turnaround_time = sum(turnaround_times.values()) / n
     avg_waiting_time = sum(waiting_times.values()) / n

     # Display Gantt chart and results
     self.plot_gantt_chart(gantt_chart, "Priority Preemptive Scheduling")
     self.display_results(
        [(name, arrival, burst) for name, arrival, burst in zip(process_names, arrival_times, burst_times)],
        list(turnaround_times.values()),
        list(waiting_times.values()),
        avg_turnaround_time,
        avg_waiting_time )
     
    def priority_non_preemptive(self, process_names, arrival_times, burst_times, priorities):
     # Combine process data into tuples
     processes = list(zip(process_names, arrival_times, burst_times, priorities))
     gantt_chart = []
     time = 0
     completed = 0
     n = len(processes)

     # Initialize metrics
     turnaround_times = {p[0]: 0 for p in processes}
     waiting_times = {p[0]: 0 for p in processes}
     end_times = {}

     # While not all processes are completed
     while completed < n:
        # Get processes that have arrived and are not completed
        available_processes = [p for p in processes if p[1] <= time and p[0] not in end_times]
        if not available_processes:
            time += 1  # Increment time if no process is available
            continue

        # Select process with the highest priority (lowest priority value)
        highest_priority_process = min(available_processes, key=lambda x: (x[3], x[1]))
        process_name, arrival_time, burst_time, _ = highest_priority_process

        # Record the start and end time of the process
        start_time = max(time, arrival_time)
        time = start_time + burst_time
        end_time = time
        gantt_chart.append((process_name, start_time, end_time))

        # Calculate metrics
        end_times[process_name] = end_time
        turnaround_times[process_name] = end_time - arrival_time
        waiting_times[process_name] = turnaround_times[process_name] - burst_time

        completed += 1  # Mark the process as completed

     # Calculate average turnaround and waiting times
     avg_turnaround_time = sum(turnaround_times.values()) / n
     avg_waiting_time = sum(waiting_times.values()) / n

     # Display Gantt chart and results
     self.plot_gantt_chart(gantt_chart, "Priority Non-Preemptive Scheduling")
     self.display_results(
        [(name, arrival, burst) for name, arrival, burst in zip(process_names, arrival_times, burst_times)],
        list(turnaround_times.values()),
        list(waiting_times.values()),
        avg_turnaround_time,
        avg_waiting_time)

    def round_robin(self, process_names, arrival_times, burst_times, quantum_time):
     # Initialize processes sorted by arrival time
     processes = list(zip(process_names, arrival_times, burst_times))
     processes.sort(key=lambda p: p[1])  # Sort by arrival time

     remaining_times = {p[0]: p[2] for p in processes}  # Remaining burst times
     arrival_dict = {p[0]: p[1] for p in processes}     # Arrival times

     time = 0
     queue = []  # Ready queue
     gantt_chart = []
     turnaround_times = {}
     waiting_times = {}

     i = 0  # Index to track arriving processes

     # Initially add processes that have arrived at time 0
     while i < len(processes) and processes[i][1] <= time:
        queue.append(processes[i][0])
        i += 1

     # Main execution loop
     while queue or i < len(processes):
        if not queue:  # If the queue is empty, jump to the next arriving process
            time = processes[i][1]
            queue.append(processes[i][0])
            i += 1

        process_name = queue.pop(0)

        # Execute process for quantum time or remaining time
        executed_time = min(quantum_time, remaining_times[process_name])
        start_time = time
        time += executed_time
        end_time = time

        # Update Gantt chart
        gantt_chart.append((process_name, start_time, end_time))
        remaining_times[process_name] -= executed_time

        # Add newly arrived processes to the queue
        while i < len(processes) and processes[i][1] <= time:
            queue.append(processes[i][0])
            i += 1

        # Re-add current process if it still has remaining burst time
        if remaining_times[process_name] > 0:
            queue.append(process_name)
        else:
            # Process completed, calculate turnaround and waiting times
            turnaround_times[process_name] = time - arrival_dict[process_name]
            waiting_times[process_name] = turnaround_times[process_name] - burst_times[process_names.index(process_name)]

     # Calculate average turnaround and waiting times
     avg_turnaround_time = sum(turnaround_times.values()) / len(processes)
     avg_waiting_time = sum(waiting_times.values()) / len(processes)

     # Plot Gantt Chart
     self.plot_gantt_chart(gantt_chart, "Round Robin Scheduling")

     # Display results
     self.display_results(
        [(name, arrival, burst) for name, arrival, burst in processes],
        list(turnaround_times.values()),
        list(waiting_times.values()),
        avg_turnaround_time,
        avg_waiting_time
     )



    def plot_gantt_chart(self, gantt_chart, title):

        process_names = [item[0] for item in gantt_chart]
        start_times = [item[1] for item in gantt_chart]
        end_times = [item[2] for item in gantt_chart]
        durations = [end - start for start, end in zip(start_times, end_times)]

        fig, ax = plt.subplots(figsize=(12, 2))
        for i, (process, start, duration) in enumerate(zip(process_names, start_times, durations)):
            ax.barh(0, duration, left=start, color='skyblue', edgecolor="black", height=0.3)
            ax.text(start + duration / 2, 0, process, va='center', ha='center', color="black", fontsize=8)

        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xlim(0, max(end_times) + 1)
        ax.set_title(title, pad=10)
        ax.set_xlabel('Time')
        ax.grid(True, axis='x', linestyle='--', linewidth=0.5, alpha=0.7)
        plt.tight_layout()
        plt.show()

    def display_results(self, processes, turnaround_times, waiting_times, avg_turnaround_time, avg_waiting_time):
        output = ""
        output += "Process\tArrival Time\t\tBurst Time\t\tTurnaround Time\t\tWaiting Time\n"
        for i, process in enumerate(processes):
            output += f"{process[0]}\t\t{process[1]}\t\t{process[2]}\t\t{turnaround_times[i]}\t\t{waiting_times[i]}\n"

        output += f"\nAverage Turnaround Time: {avg_turnaround_time:.2f}\n"
        output += f"Average Waiting Time: {avg_waiting_time:.2f}\n"

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)

root = tk.Tk()
app = SchedulerGUI(root)
root.mainloop()
