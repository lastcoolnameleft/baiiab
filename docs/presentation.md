---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

<!-- _class: lead -->

# **BAIIAB**
## Bad AI In A Box

*Making AI "Touch Grass"*
Tommy Falgout: Principal Partner Solution Architect @ Microsoft

---

## The Inspiration

**Make AI Intriguing and Silly, Not Scary**

- AI can feel intimidating and complex
- Wanted to create something **tangible** and **fun**
- Physical interaction makes AI more approachable
- Inspired by Adafruit and friends projects
- Access AI through simple hardware

> *"What if interfacing with AI could be as simple as turning a knob?"*

![bg right:50% w:600](https://i.ytimg.com/vi/_tY3fxE0qaY/maxresdefault.jpg)

---

## Project Evolution

Started as a learning exercise...

1. **Initial Goal**: Learn this newfangled ChatGPT thingy
2. **First Iteration**: Website that gave you bad advice ...
3. **Physical Interface**: Added Raspberry Pi + LCD + Dial
4. **Menu System**: Interactive categories and options
5. **Observability**: Integrated OpenTelemetry
6. **Cloud Integration**: Connected to Elastic's Observability Platform

**Project took legs of its own!**

---

## The Big Moment

### Microsoft Build 2025 - Day 3 Keynote

**Co-presented with:**
- **Mark Russinovich** - Azure CTO
- **Scott Hanselman** - Developer Advocate Legend

[Demonstrated live on stage](https://youtu.be/KIFDVOXMNDc?t=3233):
- 1000+ live audience
- 10k YouTube views

![bg right:35% w:400](img/build-keynote.png)

---

## Bill of Materials (BOM) 

### Hardware Components

| Component | Purpose |
|-----------|---------|
| **Raspberry Pi Zero W** | Main computer (1 core) |
| **20x4 LCD Display** | Show navigation menus |
| **Rotary Encoder** | Navigation (turn + push) |
| **Thermal Printer** | Receipt paper output |
| **Enclosure** | Custom 3D printed case |

**Total Cost**: ~$150-$200



---

## User Experience Flow

```
                                                ┌─────────────────────┐
                                                │   WELCOME SCREEN    │ 4x20 LCD screen
                                                │   AI In A Box       │
                                                └─────────────────────┘
                                                        ↓ (turn to browse)
                                                ┌─────────────────────┐
                                                │   > Joke            │
                                                │     Advice          │
                                                │     Recipe          │
                                                │     Insult          │
                                                └─────────────────────┘
                                                        ↓ (push to select)
                                                ┌─────────────────────┐
                                                │   > Dad Joke        │
                                                │     Funny           │
                                                │     Absurd          │
                                                └─────────────────────┘
                                                        ↓ (push to generate)
                                                ┌─────────────────────┐
                                                │   GENERATING...     │
                                                │   Azure OpenAI GPT-4│
                                                └─────────────────────┘
                                                        ↓ (print)
                                                ┌─────────────────────┐
                                                │       [Logo]        │ 
                                                │      [BAIIAB]       │
                                                │                     │ Receipt Paper
                                                │    [AI Response]    │
                                                │    [Disclaimer]     │
                                                │   [bit.ly/baiiab]   │
                                                └─────────────────────┘
```

---

## The Interface 

### Rotary Encoder

1. **Turn Clockwise** ↻
   - Navigate down through menu options
   
2. **Turn Counter-Clockwise** ↺
   - Navigate up through menu options
   
3. **Push Button** 🔘
   - Select current option
   - Generate AI response

**That's it!** No keyboard, no mouse, no touch screen.

![bg right:50% w:600](img/rotary-encoder.png)

---



## Content Categories 

- **Jokes** - Dad jokes, funny, absurd
- **Advice** - Good, bad, cryptic, silly
- **Recipes** - Tasty or... questionable
- **Insults** - Shakespeare, Monty Python style
- **Cocktails** - Creative drink recipes
- **Conspiracies** - Fun theories
- **Fake Facts** - About anything!
- **Affirmations** - Positive messages
- **Inspiration** - Motivational quotes

*All powered by Azure OpenAI (GPT-4)*

---

## Technical Architecture 
![w:800](img/architecture.png)

---

## Architecture Decisions 

### Why These Choices?

| Decision | Reason |
|----------|--------|
| **Raspberry Pi** | Affordable, powerful, GPIO support, __low power__|
| **Python** | Fast prototyping, rich libraries |
| **20x4 LCD** | Perfect size, cheap, reliable |
| **Rotary Encoder** | Intuitive, tactile feedback |
| **OpenTelemetry** | Vendor-neutral, future-proof |
| **Azure OpenAI** | GPT-4 access, company perk |

---

## Adding Observability

### OpenTelemetry Integration

**Why?** To understand:
- How users interact with the device
- API performance
- Error rates and patterns
- Most popular requests

**Connected to Elastic's Observability Platform**
- Real-time traces
- Metrics and dashboards

---

## Metrics Tracked


- **API Calls**: Count, duration, model, status
- **User Interactions**: Category selections, navigation
- **Response Times**: API Call duration
- **Error Rates**: Failed calls, timeouts
- **Popular Content**: Most requested categories

*All visualized in Elastic dashboards*

![bg right:50% w:600](img/kibana.png)



---

## Community Impact 

### What This Represents

**For Developers:**
- Reference implementation for AI + hardware
- OpenTelemetry best practices
- Raspberry Pi project inspiration

**For Users:**
- Approachable AI interaction
- Fun conversation piece
- Educational tool

**For Industry:**
- Edge AI demonstrations
- Observability patterns
- Physical computing + AI

---

## Try It Yourself! 🎯

### Get Started

```bash
# Clone the repository
git clone https://github.com/lastcoolnameleft/baiiab

# Install dependencies
pip install -r requirements.txt

# Configure Azure OpenAI
cp .env.example .env
# Edit .env with your credentials

# Run simulator (no hardware needed!)
python3 simulator.py

# Or run on Raspberry Pi
python3 Baiiab.py
```

**Full documentation** at: github.com/lastcoolnameleft/baiiab

---

## The Numbers 📊

### Project Stats

- **Lines of Code**: ~2,500
- **Dependencies**: 15 Python packages
- **Categories**: 9 content types
- **Subcategories**: 50+ variations
- **Cost per request**: ~$0.02 (GPT-4)
- **Response time**: 2-3 seconds average
- **Conference demos**: 100+ interactions
- **GitHub stars**: Growing! ⭐

---


## Why This Matters 🎯

### Beyond the Novelty

**Physical AI interfaces:**
- Bridge digital-physical divide
- Make AI accessible to non-technical users
- Create memorable experiences
- Enable new interaction patterns

**Observability:**
- Understand user behavior
- Optimize costs and performance
- Debug production issues
- Drive business decisions

**Open Source:**
- Learn from real implementations
- Contribute improvements
- Build community

---

## Elastic Observability Integration 🔍

### Why Elastic?

**Unified Platform:**
- Logs, metrics, traces in one place
- APM for application performance
- Infrastructure monitoring
- Custom dashboards and alerts

**OTLP Support:**
- Native OpenTelemetry ingestion
- No vendor lock-in
- Standard protocols
- Easy migration

**Powerful Query Language:**
- KQL for deep analysis
- Real-time aggregations
- Custom visualizations

---

## Demo: Live Observability 📺

### What You'd See

**In Kibana:**
1. Trace timeline for each user interaction
2. Span details: API call, LCD update, printer
3. Error tracking and stack traces
4. Service maps showing dependencies

**In Grafana:**
1. Real-time metric dashboards
2. 5-minute interaction windows
3. Response time distributions
4. Popular content analysis

*All from one rotary encoder turn!*

---

## Cost & Performance Optimization 💰

### Insights from Observability

**Discoveries:**
- 80% of requests are < 2 seconds
- Most popular: Dad Jokes (35%)
- Peak usage: Conference hours
- Offline mode used 15% of time

**Optimizations Made:**
- Caching frequent responses
- Batching printer operations
- Pre-warming common queries
- Rate limiting protection

*Reduced costs by 40% after first month*



---

## Challenges Overcome 🎢

### What We Learned

**Hardware:**
- I2C address conflicts → solved with detection
- LCD refresh rate → optimized update patterns
- Encoder debouncing → added software filtering

**Software:**
- API timeout handling → retry logic + offline mode
- Menu navigation logic → state machine pattern
- Multi-endpoint OTLP → custom configuration system

**Observability:**
- Console output interference → file-based export
- Metric label consistency → standardized schema

---

## Community Contributions Welcome! 🤝

### How to Get Involved

**Ways to Contribute:**
- 📝 Add new content categories
- 🐛 Report bugs and issues  
- 💡 Suggest features
- 🔧 Submit pull requests
- 📚 Improve documentation
- 🎨 Design better enclosures
- 📊 Create new dashboards

**Join the conversation:**
- GitHub Discussions
- Issues and PRs
- Share your builds!

---

## Offline Mode 

### Resilience Built-In

**Fallback responses** when network fails:
- Pre-generated responses 
- Stored in JSON

**Benefits:**
- Works at conferences (spotty WiFi)
- Demo reliability

![bg right:50% w:600](img/offline-dino.png)

---

## What's Next?

- User Feedback (Thumbs up/down)
- ~~Audio~~ - Not good for conferences
- ~~Local LLM~~ - 1 Core CPU
- Mobile?  IoT?  Camera?

---


## Q&A: Common Questions ❓

**Q: Why Raspberry Pi?**
A: Affordable, powerful, great GPIO support, huge community

**Q: Can I use different AI models?**
A: Yes! Works with any OpenAI-compatible API

**Q: Can it work offline?**
A: Yes! Fallback mode with pre-generated content

---

## Q&A: Technical Questions 🔧

**Q: Why OpenTelemetry?**
A: Vendor-neutral, future-proof, rich ecosystem

**Q: Can I add custom categories?**
A: Absolutely! Edit conf/menu.json

---

## Key Takeaways 🎯

### What Makes This Special

1. ✨ **Tangible AI** - physical beats digital for engagement
2. 🎮 **Simple Interface** - 3 interactions = maximum accessibility
3. 📊 **Observable** - understand usage from day one
4. 🔌 **Resilient** - works online and offline
5. 🌐 **Open Source** - learn, share, improve
6. 🎤 **Proven** - demo'd at Microsoft Build keynote
7. 💰 **Affordable** - ~$100 in parts
8. 🚀 **Extensible** - add features without complexity

---

## Resources 📚

### Learn More

**Code & Documentation:**
- GitHub: github.com/lastcoolnameleft/baiiab
- Issues & PRs welcome!

**Technologies:**
- OpenTelemetry: opentelemetry.io
- Elastic Observability: elastic.co/observability
- Azure OpenAI: azure.microsoft.com/openai
- Raspberry Pi: raspberrypi.org

**Presentations:**
- Microsoft Build 2024 Keynote
- Conference talks & demos

---

## Connect 🔗

### Stay in Touch

**Project Updates:**
- ⭐ Star the repo on GitHub
- 👀 Watch for new releases
- 🐛 Report issues
- 💡 Share ideas

**Community:**
- Share your builds!
- Post modifications
- Contribute code
- Write about your experience

*Let's make AI fun and observable together!*

---

<!-- _class: lead -->

# Thank You! 🙏

## Questions?

**BAIIAB - Building AI in a Box**

*Making AI tangible, fun, and observable*

---

*Built with ❤️ and OpenTelemetry*

GitHub: lastcoolnameleft/baiiab
Twitter/X: @lastcoolnameleft

