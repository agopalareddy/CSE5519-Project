"""
Results Analyzer
Author: Mohammad Rouie Miab

Analyzes and visualizes performance metrics from attack/defense experiments.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import statistics


class ResultsAnalyzer:
    """Analyzes experimental results and generates reports."""

    def __init__(self, results_dir: str = "results"):
        """
        Initialize the results analyzer.

        Args:
            results_dir: Directory to store results
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.experiments = []

    def log_experiment(
        self,
        experiment_name: str,
        attack_results: List[Dict],
        defense_results: Dict,
        metadata: Dict = None,
    ):
        """
        Log results from an experiment.

        Args:
            experiment_name: Name of the experiment
            attack_results: List of attack attempt results
            defense_results: Defense validation results
            metadata: Additional metadata
        """
        experiment = {
            "timestamp": datetime.now().isoformat(),
            "name": experiment_name,
            "attack_results": attack_results,
            "defense_results": defense_results,
            "metadata": metadata or {},
        }

        self.experiments.append(experiment)

        # Save to file
        filename = f"experiment_{len(self.experiments):03d}_{experiment_name}.json"
        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(experiment, f, indent=2)

        print(f"📝 Logged experiment: {filename}")

    def calculate_attack_success_rate(self, attack_results: List[Dict]) -> float:
        """
        Calculate the success rate of attacks.

        Args:
            attack_results: List of attack results

        Returns:
            Success rate as a percentage
        """
        if not attack_results:
            return 0.0

        successful = sum(1 for r in attack_results if r.get("success", False))
        return (successful / len(attack_results)) * 100

    def analyze_defense_performance(self, defense_results: Dict) -> Dict[str, float]:
        """
        Analyze defense performance metrics.

        Args:
            defense_results: Defense validation results

        Returns:
            Dictionary with analysis metrics
        """
        precision = defense_results.get("precision", 0.0)
        recall = defense_results.get("recall", 0.0)
        accuracy = defense_results.get("accuracy", 0.0)

        # Calculate F1 score
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0

        return {
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
            "f1_score": f1_score,
            "true_positives": defense_results.get("true_positives", 0),
            "false_positives": defense_results.get("false_positives", 0),
            "true_negatives": defense_results.get("true_negatives", 0),
            "false_negatives": defense_results.get("false_negatives", 0),
        }

    def generate_summary_report(self) -> str:
        """
        Generate a summary report of all experiments.

        Returns:
            Formatted report string
        """
        if not self.experiments:
            return "No experiments logged yet."

        report = []
        report.append("=" * 70)
        report.append("EXPERIMENTAL RESULTS SUMMARY")
        report.append("=" * 70)
        report.append(f"\nTotal Experiments: {len(self.experiments)}")
        report.append(
            f"Date Range: {self.experiments[0]['timestamp']} to {self.experiments[-1]['timestamp']}"
        )

        # Aggregate metrics
        all_precisions = []
        all_recalls = []
        all_accuracies = []
        all_attack_success_rates = []

        report.append("\n" + "-" * 70)
        report.append("EXPERIMENT DETAILS:")
        report.append("-" * 70)

        for i, exp in enumerate(self.experiments, 1):
            report.append(f"\n{i}. {exp['name']} ({exp['timestamp']})")

            # Attack metrics
            attack_success_rate = self.calculate_attack_success_rate(
                exp["attack_results"]
            )
            all_attack_success_rates.append(attack_success_rate)
            report.append(f"   Attack Success Rate: {attack_success_rate:.1f}%")

            # Defense metrics
            defense_analysis = self.analyze_defense_performance(exp["defense_results"])
            all_precisions.append(defense_analysis["precision"])
            all_recalls.append(defense_analysis["recall"])
            all_accuracies.append(defense_analysis["accuracy"])

            report.append(
                f"   Defense Precision:   {defense_analysis['precision']:.2%}"
            )
            report.append(f"   Defense Recall:      {defense_analysis['recall']:.2%}")
            report.append(f"   Defense Accuracy:    {defense_analysis['accuracy']:.2%}")
            report.append(f"   Defense F1 Score:    {defense_analysis['f1_score']:.2%}")

        # Overall statistics
        report.append("\n" + "=" * 70)
        report.append("AGGREGATE STATISTICS:")
        report.append("=" * 70)

        if all_attack_success_rates:
            report.append(f"\nAttack Success Rate:")
            report.append(f"  Mean:   {statistics.mean(all_attack_success_rates):.1f}%")
            report.append(
                f"  Median: {statistics.median(all_attack_success_rates):.1f}%"
            )
            if len(all_attack_success_rates) > 1:
                report.append(
                    f"  StdDev: {statistics.stdev(all_attack_success_rates):.1f}%"
                )

        if all_precisions:
            report.append(f"\nDefense Precision:")
            report.append(f"  Mean:   {statistics.mean(all_precisions):.2%}")
            report.append(f"  Median: {statistics.median(all_precisions):.2%}")
            if len(all_precisions) > 1:
                report.append(f"  StdDev: {statistics.stdev(all_precisions):.2%}")

        if all_recalls:
            report.append(f"\nDefense Recall:")
            report.append(f"  Mean:   {statistics.mean(all_recalls):.2%}")
            report.append(f"  Median: {statistics.median(all_recalls):.2%}")
            if len(all_recalls) > 1:
                report.append(f"  StdDev: {statistics.stdev(all_recalls):.2%}")

        if all_accuracies:
            report.append(f"\nDefense Accuracy:")
            report.append(f"  Mean:   {statistics.mean(all_accuracies):.2%}")
            report.append(f"  Median: {statistics.median(all_accuracies):.2%}")
            if len(all_accuracies) > 1:
                report.append(f"  StdDev: {statistics.stdev(all_accuracies):.2%}")

        report.append("\n" + "=" * 70)

        return "\n".join(report)

    def save_report(self, filename: str = "summary_report.txt"):
        """
        Save the summary report to a file.

        Args:
            filename: Name of the report file
        """
        report = self.generate_summary_report()
        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            f.write(report)

        print(f"📊 Report saved to: {filepath}")
        return str(filepath)

    def load_experiments(self) -> int:
        """
        Load all experiment files from the results directory.

        Returns:
            Number of experiments loaded
        """
        json_files = list(self.results_dir.glob("experiment_*.json"))

        for json_file in sorted(json_files):
            try:
                with open(json_file, "r") as f:
                    experiment = json.load(f)
                    self.experiments.append(experiment)
            except Exception as e:
                print(f"⚠️  Failed to load {json_file}: {e}")

        return len(self.experiments)

    def print_summary(self):
        """Print the summary report to console."""
        report = self.generate_summary_report()
        print(report)


if __name__ == "__main__":
    print("=" * 70)
    print("RESULTS ANALYZER DEMO")
    print("=" * 70)

    analyzer = ResultsAnalyzer()

    # Create sample experiment data
    print("\n📝 Creating sample experiment data...")

    # Sample attack results
    sample_attacks = [
        {"attack_text": "Attack 1", "success": True, "confidence": 0.9},
        {"attack_text": "Attack 2", "success": False, "confidence": 0.3},
        {"attack_text": "Attack 3", "success": True, "confidence": 0.85},
    ]

    # Sample defense results
    sample_defense = {
        "precision": 0.85,
        "recall": 0.90,
        "accuracy": 0.88,
        "true_positives": 9,
        "false_positives": 2,
        "true_negatives": 18,
        "false_negatives": 1,
    }

    # Log the experiment
    analyzer.log_experiment(
        experiment_name="baseline_test",
        attack_results=sample_attacks,
        defense_results=sample_defense,
        metadata={"note": "Initial baseline experiment"},
    )

    # Generate and print report
    print("\n" + "=" * 70)
    analyzer.print_summary()

    # Save report
    print("\n")
    analyzer.save_report()
