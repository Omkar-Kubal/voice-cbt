# 🤖 LLM Setup Guide for ChatGPT-like Responses

This guide helps you configure the Voice CBT system to generate dynamic, ChatGPT-like responses instead of basic repetitive ones.

## 🚀 Quick Setup Options

### Option 1: OpenAI API (Recommended - Best Results)
1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   export OPENAI_MODEL="gpt-3.5-turbo"  # or gpt-4 for better responses
   ```
3. Restart the backend: `docker-compose restart backend`

### Option 2: Local LLM (Free but requires setup)
1. Install Ollama: https://ollama.ai/
2. Pull a model: `ollama pull llama2`
3. Set environment variables:
   ```bash
   export USE_LOCAL_LLM="true"
   export LOCAL_LLM_URL="http://localhost:11434"
   ```
4. Start Ollama: `ollama serve`
5. Restart the backend: `docker-compose restart backend`

### Option 3: No LLM (Fallback - Current System)
The system will automatically fall back to the enhanced rule-based responses if no LLM is configured.

## 🔧 Configuration Details

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (gpt-3.5-turbo, gpt-4, etc.)
- `USE_LOCAL_LLM`: Set to "true" to use local LLM
- `LOCAL_LLM_URL`: URL for local LLM server

### Response Quality Comparison
- **OpenAI GPT**: Most natural, ChatGPT-like responses
- **Local LLM**: Good responses, but may be slower
- **Fallback**: Enhanced but still rule-based responses

## 🎯 Expected Improvements

With LLM integration, you'll get:
- ✅ Dynamic, contextual responses
- ✅ No more repetitive generic messages
- ✅ Natural conversation flow
- ✅ Personalized follow-up questions
- ✅ Context-aware suggestions
- ✅ ChatGPT-like interaction quality

## 🚨 Troubleshooting

### If responses are still basic:
1. Check if environment variables are set correctly
2. Verify API key is valid (for OpenAI)
3. Check backend logs for LLM integration errors
4. Ensure local LLM is running (if using local option)

### Backend logs will show:
- `🧠 LLM generated response:` - LLM is working
- `⚠️ LLM integration failed:` - Falling back to rule-based system
