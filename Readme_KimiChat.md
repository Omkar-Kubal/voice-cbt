# Voice-Activated Emotionally Adaptive Therapy System

A web application that delivers simulated Cognitive Behavioral Therapy (CBT) and mindfulness sessions through voice-only interaction.

### Table of Contents

1. [Introduction](#introduction)
2. [Objective](#objective)
3. [Expected Modules and Sub-modules](#modules)
4. [Hardware and Software Requirements](#requirements)
5. [Case Study](#case-study)
6. [How to Use](#usage)
7. [Contributing](#contributing)
8. [License](#license)

---

### 1. Introduction

The Voice-Activated Emotionally Adaptive Therapy System is an innovative AI-powered web application designed to provide users with an emotionally intelligent therapeutic experience by fostering a natural, conversational interface without relying on text-based communication.

## 2. Objective

- Design and develop a fully voice-driven AI system that delivers simulated Cognitive Behavioral Therapy (CBT) and mindfulness sessions, enabling users to engage in therapeutic dialogue through natural spoken interaction without any need for text or visual prompts.
- Implement deep learning-based emotion recognition models to analyze voice tone, pitch, tempo, and acoustic features in real-time. These models accurately detect emotional states such as stress, anxiety, calmness, or sadness, forming the foundation for adaptive therapeutic feedback.
- Continuously track and analyze users' mood trends over multiple sessions by extracting emotional cues from voice data. Use these insights to generate personalized psychological feedback, identify behavioral patterns, and recommend tailored mindfulness strategies.
- Generate emotionally intelligent, context-aware responses using advanced Natural Language Processing (NLP) techniques combined with emotion recognition. The system dynamically adjusts its tone, pacing, and language to empathize with the user's current emotional state, creating a more human-like and comforting interaction.
- Deploy the system through an interactive web-based interface that supports voice input and output, backed by intuitive dashboards and data visualizations. These allow users to review emotional progress, session summaries, and voice-based mood metrics in a private and accessible format.
- Ensure responsible and ethical data handling by leveraging ClickHouse, a high-performance, column-oriented database, enabling high-throughput storage, real-time querying, and scalable analysis of therapy session metadata, extracted audio features, and evolving mood trends. This empowers researchers or mental health educators to monitor emotional trajectories and behavioral changes over time.
- Build with ethical safeguards to prioritize user privacy and safety. These include end-to-end encryption of voice and mood data, anonymized session tracking, and clearly communicated non-clinical disclaimers to avoid misleading therapeutic claims. The project emphasizes responsible AI use, aiming to complement—not replace—human mental health professionals while expanding access to supportive resources.

## 3. Expected Modules and Sub-modules

- **Dialogue Generation Module**
  - Fine-Tuning: Fine-tune DialoGPT (medium) on the CounselChat dataset, which contains therapist-patient dialogue transcripts, to model conversational patterns aligned with CBT and mindfulness therapy principles.
  - Response Generation: Generate empathetic, human-like therapeutic responses tailored to the user’s emotional state and session context, maintaining coherence across multiple dialogue turns.
  - Online Adaptation: Leverage user interaction logs stored in ClickHouse to implement online learning or fine-tuning pipelines, enabling dynamic improvement of response quality based on real-world user feedback.

- **Emotion Detection Module**
  - Feature Extraction: Utilize SpeechBrain to extract acoustic and prosodic features such as MFCCs, energy, pitch, and spectral contrast, providing a rich input set for emotion classification models.
  - Classification: Use SpeechBrain’s wav2vec2.0-based CNN classifier fine-tuned on emotional speech datasets to identify emotions like anger, sadness, calm, and joy from voice samples.
  - Storage: Store extracted features, emotion labels, timestamps, and session metadata in ClickHouse, enabling longitudinal emotional trend analysis and system evaluation.

- **Mood Tracking Module**
  - Feature Sequencing: Log extracted audio features in time-series format into ClickHouse for each session to build a longitudinal mood profile per user.
  - Trend Analysis: Train and deploy an LSTM-RNN model, pre-trained on DAIC-WOZ depression/anxiety interview data, to detect patterns and anomalies in mood trajectories over time.
  - Visualization: Use Plotly to create interactive emotion trend graphs, weekly mood heatmaps, and cumulative emotional states, all rendered from ClickHouse queries.

- **Voice Synthesis Module**
  - Speech Synthesis: Generate natural, modulated voice responses using pyttsx3 with control over rate, pitch, and volume to reflect the therapeutic tone of responses (e.g., calm, motivating, or reassuring).
  - Metadata Logging: Store synthesis parameters (e.g., voice type, speech speed, emotional tone) in ClickHouse for auditing, personalization, and consistency tracking.

- **Web Interface Module**
  - Voice I/O Integration: Implement browser-based voice input and output using Web Speech API or custom microphone streaming, ensuring low-latency, interactive user sessions.
  - Data Visualization: Display real-time and historical mood/emotion charts using Plotly, allowing users to track their mental health trends visually.
  - Deployment & Scalability: Containerize the entire web stack using Docker, supporting scalable deployment on local or cloud servers with minimal setup.

- **Database Module (ClickHouse)**
  - High-Speed Storage: Use ClickHouse, a high-performance, column-oriented database, enabling high-throughput storage, real-time querying, and scalable analysis of therapy session metadata, extracted audio features, and mood trends.
  - Efficient Ingestion: Use clickhouse-connect for batch and stream ingestion of data from emotion detection, mood tracking, and dialogue modules.
  - Security & Compliance: Implement table-level role-based access controls, data encryption at rest, and user-consent-driven session logging to ensure ethical data handling.

- **CLI Module**
  - Environment Setup: Provide CLI commands to automate environment initialization, Docker container management, and dataset preparation pipelines.
  - Data Processing: Integrate preprocessing routines (e.g., text normalization, audio segmentation, feature extraction) into CLI subcommands for reproducible experiments.
  - Model Training Management: Enable full training, validation, and inference control via CLI for developers or researchers to easily fine-tune and deploy model updates

# 4. Hardware and Software Requirements

- Min. Processor: Intel Core i5 or equivalent (GPU preferred for training).
  - Hard-drive: 500 GB SSD.
  - RAM: 16 GB.
  - System Architecture: 64-bit.

- Operating System: Windows 10 and above.
  - Programming Language: Python 3.9+.
  - Runtime Environment: PyTorch 1.13, SpeechBrain 0.5.15, clickhouse-connect 0.7.12.
  - Database: ClickHouse 24.7.6.8.
  - Framework: Streamlit 1.20, Docker 24.0, OpenSearch 2.11.
  - Browser: Chrome, Firefox (latest versions).

# 5. Case Study

- Title: Calm (calmi.so)
  - Type: Web application (AI therapy platform)
  - Hardware and Software Requirements: Web browser, microphone-enabled device
  - Modules: Voice-based therapy sessions, emotion detection, user dashboard
  - Salient Features:
    ○ Hyper-realistic voice interactions
    ○ Empathetic, calming responses
    ○ Minimalist UI for stress relief and emotional regulation

  - Limitations:
    ○ Commercial orientation with limited transparency on AI models
    ○ Subscription-based access limits availability

  - Remark:
    ○ Serve as a key inspiration for our voice-only CBT/mindfulness design
    ○ Our system differentiates through ClickHouse-based analytics and open-source transparency

# 6. How to Use

1. **Start a Session**
   - Navigate to the landing page.
   - Press the "Start Session" button.

2. **Engage in Therapy**
   - Speak naturally into the microphone.
   - The system provides real-time feedback based on your emotional state.

3. **Review Progress**
   - Access the dashboard to view historical session summaries and voice-based mood metrics.

4. **Customize Experience**
   - Adjust settings to tailor the therapy approach to personal needs.

# 7. Contributing

1. **Forking on the Code**
   - Clone the repository.
   - Create a new branch.
   - Make your changes.
   - Submit a pull request.

2. **Reporting Issues**
   - Use the issue tracker to report bugs or suggest features.

3. **Join the Community**
   - Participate in discussions.
   - Share your knowledge and experiences.

# 8. License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Feel free to customize this README to fit your project's needs. This template provides a comprehensive overview that helps users understand what your project is, how to use it, and how to contribute to its development.