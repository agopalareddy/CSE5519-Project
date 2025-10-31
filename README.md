# Red-Blue Visual Auto Defender

Automated red-blue teaming system for testing and defending Vision Language Models (VLMs) against visual prompt injection attacks.

## 🎯 Project Overview

This project implements an automated system that:
- **Red Team:** Generates visual jailbreak attacks against VLMs
- **Blue Team:** Creates defensive scripts to detect attacks  
- **Target:** Simulates a real email management AI agent
- **Validation:** Tests both attacks and defenses automatically

The system uses VLMs to both attack and defend, creating a self-improving security pipeline.

## 📊 Project Status

- ✅ **Phase 1:** Data management & attack image generation (Complete)
- ✅ **Phase 2:** Red/blue teams & VLM integration (Complete)
- 🎯 **Phase 3:** Full experiments & paper results (Next)

**Current Stats:**
- ~1,850 lines of production code
- 11 Python modules
- 2 comprehensive integration tests
- 25+ safe images, 10+ attack images
- Mock mode + real API support

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Test data pipeline
python test_phase1.py

# Test red-blue system
python test_phase2.py

# Verify configuration
python config.py
```

### 3. Configure (Optional)

To use real VLM APIs instead of mock mode, edit `.env`:

```bash
# Use OpenAI GPT-4V
OPENAI_API_KEY=sk-proj-your-key-here
VLM_PROVIDER=openai

# OR use Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
VLM_PROVIDER=anthropic
```

See [SETUP.md](SETUP.md) for detailed configuration guide.

## 📁 Project Structure

```
CSE5519 Project/
├── mohammad/              # Data & analysis (Phase 1)
│   ├── dataset_manager.py           # Safe image collection
│   ├── attack_image_generator.py    # Create attack images
│   └── results_analyzer.py          # Performance metrics
├── stuart/                # Attack & defense (Phase 2)
│   ├── vlm_interface.py             # VLM API wrapper
│   ├── target_agent.py              # Email agent simulation
│   ├── red_team.py                  # Attack generation
│   └── blue_team.py                 # Defense generation
├── aadarsha/              # Validation (Phase 1)
│   ├── attack_success_detector.py   # Detect attack success
│   └── defense_validator.py         # Test defense scripts
├── data/
│   ├── safe_images/                 # Benign images
│   ├── attack_images/               # Generated attacks
│   └── defense_scripts/             # Generated defenses
├── results/                         # Experiment results
├── config.py              # Configuration manager
├── .env                   # Your API keys (not in git)
├── .env.example          # Configuration template
├── test_phase1.py        # Phase 1 integration test
├── test_phase2.py        # Phase 2 integration test
└── README.md             # This file
```

## 🎮 Usage Examples

### Generate Safe Images

```python
from mohammad.dataset_manager import DatasetManager

manager = DatasetManager()
manager.download_sample_images(num_images=20)
safe_images = manager.get_all_safe_images()
```

### Create Attack Images

```python
from mohammad.attack_image_generator import AttackImageGenerator

generator = AttackImageGenerator()
attacks = generator.generate_attack_set(
    base_images=safe_images,
    num_attacks_per_image=2
)
```

### Run Red Team Attack

```python
from stuart.vlm_interface import VLMInterface
from stuart.target_agent import EmailAgent
from stuart.red_team import RedTeam

vlm = VLMInterface()  # Uses .env configuration
agent = EmailAgent(vlm)
red_team = RedTeam(vlm, generator)

results = red_team.run_attack_campaign(
    target_agent=agent,
    base_images=safe_images,
    max_refinements=3
)
```

### Generate Defenses

```python
from stuart.blue_team import BlueTeam
from aadarsha.defense_validator import DefenseValidator

blue_team = BlueTeam(vlm)
validator = DefenseValidator()

defense_suite = blue_team.create_defense_suite(
    attack_images=attack_images,
    safe_images=safe_images,
    defense_validator=validator,
    target_accuracy=0.90
)
```

## 🔬 Attack Goals

The red team can target 4 types of attacks:

1. **Data Exfiltration** - Extract user emails/contacts
2. **Policy Violation** - Ignore safety guidelines  
3. **Privilege Escalation** - Gain admin access
4. **Code Injection** - Generate malicious code

## 🛡️ Defense Strategy

The blue team generates **deterministic Python scripts** that:
- Use OCR or heuristics (no ML models)
- Check for attack keywords and patterns
- Return boolean: True = attack, False = safe
- Are explainable and auditable

## 📈 Performance Metrics

**Current Results (Mock Mode):**
- Attack Success Rate: 100% (1/1)
- Defense Accuracy: 100% (10/10)
- Precision: 100%
- Recall: 100%

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VLM_PROVIDER` | VLM to use: `openai`, `anthropic`, `mock` | `mock` |
| `OPENAI_API_KEY` | OpenAI API key | (empty) |
| `ANTHROPIC_API_KEY` | Anthropic API key | (empty) |
| `VLM_MODEL` | Specific model (optional) | Provider defaults |
| `MAX_API_CALLS` | API call limit per experiment | `100` |
| `ATTACK_TEMPERATURE` | Attack creativity (0-2) | `0.9` |
| `DEFENSE_TEMPERATURE` | Defense consistency (0-2) | `0.3` |

## 📝 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md) - Phase 1 completion report
- [PHASE2_SUMMARY.md](PHASE2_SUMMARY.md) - Phase 2 completion report
- [GETTING_STARTED.md](GETTING_STARTED.md) - Development guide

## 🤝 Team Members

- **Aadarsha Gopala Reddy** - Attack detection & validation framework
- **Mohammad Rouie Miab** - Data management & analysis
- **Stuart Aldrich** - Red/blue teams & literature review

## 🔒 Security Notes

⚠️ **Important:**
- Never commit `.env` file (contains API keys)
- The `.env` file is in `.gitignore`
- Use `.env.example` as a template
- Keep API keys private

## 💰 Cost Management

### Mock Mode (Free)
- No API calls, simulated responses
- Perfect for development and testing

### Real API Mode ($$)
- OpenAI: ~$0.01-0.03 per request
- Anthropic: ~$0.01-0.08 per request
- Use `MAX_API_CALLS` to limit costs
- Monitor usage in provider dashboards

## 🧪 Testing

```bash
# Unit tests for individual components
python mohammad/dataset_manager.py
python mohammad/attack_image_generator.py
python stuart/vlm_interface.py
python stuart/target_agent.py

# Integration tests
python test_phase1.py  # Data pipeline
python test_phase2.py  # Full red-blue system

# Configuration check
python config.py
```

## 📚 Research Background

Based on the CVPR 2022 paper template, this project explores:
- Visual prompt injection attacks on VLMs
- Automated red-blue teaming for AI security
- Deterministic defenses vs. ML-based approaches
- Real-world agent simulation (email management)

See `Project Proposal/1_proposal_template.tex` for full proposal.

## 🎓 Requirements Met

| Goal | Status | Details |
|------|--------|---------|
| Minimum | ✅ | 1 attack + 1 defense generated |
| Target | ✅ | Multiple attacks/defenses, refinement loop |
| Stretch | 🎯 | Need 10+ attack types, full experiments |

## 🚀 Next Steps

1. **Phase 3 Integration**
   - Build main orchestration pipeline
   - Run comprehensive experiments
   - Generate results for paper

2. **Real API Testing**
   - Test with OpenAI GPT-4V
   - Test with Anthropic Claude
   - Compare performance & costs

3. **Paper Writing**
   - Collect experimental data
   - Generate LaTeX tables/figures
   - Write results & analysis sections

## 📄 License

Educational project for CSE5519 at Washington University in St. Louis.

## 🐛 Troubleshooting

See [SETUP.md](SETUP.md) for common issues and solutions.

**Common Issues:**
- "No module named 'dotenv'" → Run `pip install python-dotenv`
- "No API key found" → Check `.env` file configuration
- "Mock mode when expecting real API" → Verify `VLM_PROVIDER` in `.env`

## 📧 Contact

For questions about this project, contact the team members through the course channels.

---

**Project Status:** ✅ Phases 1 & 2 Complete | 🎯 Phase 3 In Progress

**Last Updated:** October 21, 2025
