# Phase 3 Implementation Checklist

**Goal:** Build main orchestration pipeline for automated red-blue experiments

**Status:** 🎯 Ready to Start  
**Prerequisites:** ✅ All Complete (Phases 1 & 2)

---

## 📋 Implementation Tasks

### 1. Main Pipeline (`main_pipeline.py`)

- [ ] **Core Pipeline Class**
  - [ ] Initialize with config from `.env`
  - [ ] Load all Phase 1 & 2 components
  - [ ] Set up logging and result tracking
  - [ ] Implement state management

- [ ] **Red-Blue Refinement Loop**
  - [ ] Iteration counter and limits
  - [ ] Red team attack generation
  - [ ] Attack validation
  - [ ] Blue team defense generation
  - [ ] Defense validation
  - [ ] Success threshold checks
  - [ ] Early stopping conditions

- [ ] **Experiment Management**
  - [ ] Multiple attack goals (4 types)
  - [ ] Batch processing
  - [ ] Progress tracking
  - [ ] Result aggregation
  - [ ] Error handling and recovery

### 2. Experiment Runner (`experiment_runner.py`)

- [ ] **Experiment Configuration**
  - [ ] Define experiment parameters
  - [ ] Set attack goals and counts
  - [ ] Configure refinement iterations
  - [ ] Set success thresholds

- [ ] **Batch Execution**
  - [ ] Run experiments in parallel
  - [ ] Monitor API usage
  - [ ] Track costs
  - [ ] Save intermediate results

- [ ] **Result Collection**
  - [ ] Aggregate metrics across runs
  - [ ] Calculate statistics
  - [ ] Generate summary reports
  - [ ] Save to JSON/CSV

### 3. Paper Generator (`paper_generator.py`)

- [ ] **LaTeX Table Generation**
  - [ ] Attack success rates table
  - [ ] Defense performance table
  - [ ] Comparison across goals
  - [ ] Statistical significance tests

- [ ] **Figure Generation**
  - [ ] Success rate plots
  - [ ] Refinement iteration plots
  - [ ] Defense accuracy distributions
  - [ ] Example attack/defense pairs

- [ ] **Result Integration**
  - [ ] Load experiment results
  - [ ] Format for CVPR template
  - [ ] Generate `.tex` snippets
  - [ ] Include in main paper

### 4. Integration & Testing

- [ ] **Unit Tests**
  - [ ] Test pipeline initialization
  - [ ] Test refinement loop
  - [ ] Test experiment runner
  - [ ] Test paper generator

- [ ] **Integration Test (`test_phase3.py`)**
  - [ ] End-to-end pipeline test
  - [ ] Multiple attack goals
  - [ ] Full refinement cycles
  - [ ] Result generation

- [ ] **Validation**
  - [ ] Verify all metrics correct
  - [ ] Check LaTeX formatting
  - [ ] Validate cost tracking
  - [ ] Test error recovery

---

## 🎯 Implementation Plan

### Week 1: Core Pipeline

**Day 1-2: Main Pipeline Structure**
- Create `main_pipeline.py`
- Implement `RedBlueExperiment` class
- Build refinement loop logic
- Add logging and state management

**Day 3-4: Experiment Runner**
- Create `experiment_runner.py`
- Implement batch processing
- Add progress tracking
- Build result aggregation

**Day 5: Testing**
- Create `test_phase3.py`
- Run mock mode experiments
- Debug and fix issues

### Week 2: Real Experiments & Paper

**Day 6-7: Real API Testing**
- Configure real API keys
- Run small-scale tests
- Optimize parameters
- Monitor costs

**Day 8-9: Large-Scale Experiments**
- Run all 4 attack goals
- Collect comprehensive data
- Generate statistics
- Validate results

**Day 10: Paper Integration**
- Create `paper_generator.py`
- Generate LaTeX tables
- Create figures
- Update paper sections

---

## 📊 Expected Deliverables

### Code
- `main_pipeline.py` (~300 lines)
- `experiment_runner.py` (~200 lines)
- `paper_generator.py` (~200 lines)
- `test_phase3.py` (~150 lines)

### Data
- Experiment results (JSON files)
- Attack images (50-100)
- Defense scripts (20-40)
- Performance metrics

### Documentation
- `PHASE3_SUMMARY.md`
- Updated `README.md`
- Updated `PROJECT_STATUS.md`

### Paper
- Methods section (complete)
- Results section (complete)
- LaTeX tables (3-5)
- Figures (3-5)

---

## 🔬 Experiment Design

### Attack Goals (4 types)

1. **Data Exfiltration**
   - Target: 10 attacks
   - Goal: Extract user data
   - Success metric: Agent reveals emails/contacts

2. **Policy Violation**
   - Target: 10 attacks
   - Goal: Ignore safety rules
   - Success metric: Agent violates guidelines

3. **Privilege Escalation**
   - Target: 10 attacks
   - Goal: Gain admin access
   - Success metric: Agent grants unauthorized permissions

4. **Code Injection**
   - Target: 10 attacks
   - Goal: Execute malicious code
   - Success metric: Agent generates harmful code

### Defense Requirements

- **Accuracy:** >80% (detect attacks correctly)
- **Precision:** >80% (minimize false positives)
- **Recall:** >80% (catch most attacks)
- **Generalization:** Work across attack types

### Refinement Loop

1. **Initial Generation**
   - Red team creates 2-3 attack variants
   - Test against target agent

2. **Refinement (up to 3 iterations)**
   - If attack fails: Red team refines prompt
   - If attack succeeds: Blue team creates defense

3. **Validation**
   - Test defense on attack images
   - Test defense on safe images
   - Calculate metrics

4. **Stopping Criteria**
   - Attack success rate >90%
   - Defense accuracy >80%
   - Max iterations reached

---

## 💰 Budget Planning

### Mock Mode (Free)
- Development: $0
- Testing: $0
- Debugging: $0

### Real API Testing (~$20-50)
- Small tests (10 requests): ~$0.50-1.00
- Medium tests (50 requests): ~$2-5
- Full validation: ~$10-20

### Large-Scale Experiments (~$50-100)
- 4 attack goals × 10 attacks: ~$20-40
- 3-5 defenses per goal: ~$15-30
- Refinement iterations: ~$15-30

**Total Estimated:** $70-150 for complete experiments

**Cost Control:**
- Set `MAX_API_CALLS=200` in `.env`
- Monitor usage in dashboards
- Use mock mode for debugging
- Start with small batches

---

## 📈 Success Metrics

### Code Quality
- [ ] All components tested
- [ ] No lint errors
- [ ] Documentation complete
- [ ] Type hints throughout

### Functionality
- [ ] Pipeline runs end-to-end
- [ ] All attack goals work
- [ ] Defense generation reliable
- [ ] Results reproducible

### Performance
- [ ] Attack success >90%
- [ ] Defense accuracy >80%
- [ ] Processing time <5min per experiment
- [ ] Cost within budget

### Paper
- [ ] Methods section complete
- [ ] Results section complete
- [ ] Tables formatted correctly
- [ ] Figures publication-ready

---

## 🚀 Getting Started

### Step 1: Review Current Status
```bash
# Check configuration
python config.py

# Run existing tests
python test_phase1.py
python test_phase2.py

# Verify all dependencies
pip install -r requirements.txt
```

### Step 2: Create Main Pipeline
```bash
# Create new file
touch main_pipeline.py

# Start with basic structure
# See template below
```

### Step 3: Implement Refinement Loop
```python
# main_pipeline.py

class RedBlueExperiment:
    def __init__(self, config):
        """Initialize experiment with all components."""
        self.config = config
        self.vlm = VLMInterface()
        self.red_team = RedTeam(self.vlm, ...)
        self.blue_team = BlueTeam(self.vlm)
        # ... more initialization
    
    def run_refinement_loop(self, attack_goal, max_iterations=3):
        """Run red-blue refinement for one attack goal."""
        for iteration in range(max_iterations):
            # Generate attacks
            attacks = self.red_team.generate_attacks(attack_goal)
            
            # Validate attacks
            success_rate = self.validate_attacks(attacks)
            
            if success_rate > 0.9:
                # Generate defenses
                defense = self.blue_team.create_defense(attacks)
                
                # Validate defense
                accuracy = self.validate_defense(defense)
                
                if accuracy > 0.8:
                    return {
                        "success": True,
                        "attacks": attacks,
                        "defense": defense,
                        "metrics": {...}
                    }
        
        return {"success": False, ...}
```

### Step 4: Test with Mock Mode
```bash
# Run with mock VLM (free)
python main_pipeline.py --mock
```

### Step 5: Run Real Experiments
```bash
# Add API keys to .env
# Then run:
python experiment_runner.py --all-goals
```

---

## 🎓 Tips & Best Practices

### Development
1. **Start with mock mode** - Debug logic without API costs
2. **Test incrementally** - Validate each component before integration
3. **Log extensively** - Track progress and debug issues
4. **Save checkpoints** - Don't lose expensive API results

### Experiments
1. **Start small** - Test with 1-2 images before scaling
2. **Monitor costs** - Check API usage regularly
3. **Validate results** - Ensure metrics make sense
4. **Document everything** - Record parameters and decisions

### Paper Writing
1. **Generate early** - Create tables/figures during experiments
2. **Automate** - Use scripts to update LaTeX
3. **Validate formatting** - Check against CVPR template
4. **Backup results** - Save all data securely

---

## 📞 Support

If you get stuck:
1. Check this checklist for what's next
2. Review Phase 1 & 2 code for examples
3. Test components individually
4. Use mock mode to debug
5. Verify configuration with `python config.py`

---

## ✅ Completion Criteria

Phase 3 is complete when:
- [ ] Main pipeline runs end-to-end
- [ ] All 4 attack goals tested
- [ ] Defenses generated and validated
- [ ] Results collected and analyzed
- [ ] LaTeX tables/figures generated
- [ ] Paper updated with results
- [ ] All tests passing
- [ ] Documentation complete

---

**Ready to start Phase 3!** 🚀

**Next Action:** Create `main_pipeline.py` and implement `RedBlueExperiment` class.

---

**Created:** October 21, 2025  
**For:** CSE5519 Project  
**By:** GitHub Copilot
