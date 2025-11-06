# TCP-Congestion-Control-Project
**Project Aim:**

The main aim of this project is to predict network congestion in TCP (Transmission Control Protocol) connections using machine learning techniques. By proactively identifying congestion before it severely impacts network performance, this approach allows for smarter and faster adaptations, improving overall reliability and efficiency of data transmission in computer networks.​​

**Project Overview & Main Points:**

Traditional TCP congestion control is reactive: Standard TCP algorithms (like Reno, Cubic) detect and respond to congestion only after packet loss or increased delays occur.

Machine learning adds proactive prediction: This project uses machine learning to analyze real-time TCP metrics (e.g., window size, round trip time, packet loss) and predict congestion before it happens.​​

Model Training: The AI model is trained on simulated or real-world TCP network data with features such as RTT, throughput, window size, and packet loss rates.

Model Output: The trained classifier predicts if a TCP flow is likely to become congested, allowing early intervention.​

Interactive Dashboard: A Streamlit-based web dashboard lets users visualize data features, make predictions, and explore congestion-related metrics interactively.

Outcome: This enables network devices or administrators to take preemptive action, potentially reducing packet loss, improving throughput, and minimizing latency.

**Key Uses and Benefits:**

Early Congestion Detection: Identifies potential for congestion before packet loss occurs, leading to proactive measures.​

Increased Network Efficiency: Improves overall throughput and reduces delays in both simulated and real-world networks.​

Adaptability: AI models can be trained to adapt to various network conditions or transport environments (wired, wireless, IoT, etc.).​

Visualization and Analysis: Streamlit dashboard allows users to dynamically explore and visualize TCP data, monitor features, and interpret model predictions.

Automation: The project can be integrated into network management tools for real-time monitoring and automated congestion control.
