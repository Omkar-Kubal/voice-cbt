# Therapy Session Page

This directory contains the main therapy session page (`App.tsx`) and its supporting components.

## Overview

The therapy session page is a voice-first, single-page application that provides a minimalist interface for users to engage in therapeutic conversations. It supports both voice and text input methods, with real-time speech-to-text and text-to-speech capabilities.

## Components

### App.tsx
The main therapy session page that manages:
- Conversation state and message history
- Voice and text input modes
- API integration with the backend
- Text-to-speech functionality with female voice selection
- Speech recognition for voice input

### VoiceSphere.tsx
A central interactive component that:
- Displays a prominent microphone icon when idle
- Shows real-time waveform visualization during listening
- Provides visual feedback for different states (listening, processing, speaking)
- Handles voice input initiation and stopping

### TextInput.tsx
A text-based input component that:
- Provides a chat-like text area for typing messages
- Supports multi-line input with proper formatting
- Includes character count and helpful tips
- Handles keyboard shortcuts (Enter to send, Shift+Enter for new line)

### ChatHistory.tsx
A conversation display component that:
- Shows the complete conversation history
- Differentiates between user and system messages
- Displays emotion indicators for system responses
- Provides timestamps and visual avatars
- Auto-scrolls to show the latest messages

## Features

### Voice-First Design
- Central voice sphere for easy access
- Real-time waveform visualization during listening
- Automatic speech-to-text conversion
- Female voice text-to-speech responses

### Text Support
- Alternative text input for users who prefer typing
- Rich text formatting support
- Keyboard shortcuts for efficiency

### API Integration
- Sends voice data as base64-encoded audio
- Sends text data as plain text
- Handles backend responses with emotion detection
- Error handling and user feedback

### Accessibility
- Clear visual states for all interactions
- Keyboard navigation support
- Screen reader friendly components
- High contrast design elements

## Usage

1. Navigate to `/app` after completing onboarding
2. Choose between voice or text input modes
3. For voice: Click the central sphere to start/stop recording
4. For text: Type in the text area and press Enter to send
5. Listen to AI responses via text-to-speech
6. View conversation history in the chat area

## Technical Details

- Built with React and TypeScript
- Uses Web Speech API for speech recognition and synthesis
- Integrates with backend API at `http://localhost:8000/api/v1/session/start`
- Responsive design with dark theme
- Modular component architecture for maintainability
