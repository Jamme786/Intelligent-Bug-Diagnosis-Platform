import pandas as pd


class DefectPatternAnalytics:

    def __init__(self, bugs=None):
        self.bugs = bugs if bugs is not None else []

    def add_bug(self, bug):
        if isinstance(bug, dict):
            self.bugs.append(bug)

    def to_dataframe(self):
        if not self.bugs:
            return pd.DataFrame()

        return pd.DataFrame(self.bugs)

    def severity_distribution(self):
        df = self.to_dataframe()

        if df.empty or "severity" not in df.columns:
            return {}

        return df["severity"].fillna("Unknown").value_counts().to_dict()

    def priority_distribution(self):
        df = self.to_dataframe()

        if df.empty or "priority" not in df.columns:
            return {}

        return df["priority"].fillna("Unknown").value_counts().to_dict()

    def component_distribution(self):
        df = self.to_dataframe()

        if df.empty or "component" not in df.columns:
            return {}

        return df["component"].fillna("Unknown").value_counts().to_dict()

    def exception_distribution(self):
        df = self.to_dataframe()

        if df.empty or "exception_type" not in df.columns:
            return {}

        return df["exception_type"].fillna("Unknown").value_counts().to_dict()

    def root_cause_distribution(self):
        df = self.to_dataframe()

        if df.empty or "root_cause" not in df.columns:
            return {}

        return df["root_cause"].fillna("Unknown").value_counts().to_dict()

    def duplicate_distribution(self):
        df = self.to_dataframe()

        if df.empty or "duplicate_status" not in df.columns:
            return {}

        return df["duplicate_status"].fillna("Unknown").value_counts().to_dict()

    def get_summary(self):
        return {
            "total_bugs": len(self.bugs),
            "severity_distribution": self.severity_distribution(),
            "priority_distribution": self.priority_distribution(),
            "component_distribution": self.component_distribution(),
            "exception_distribution": self.exception_distribution(),
            "root_cause_distribution": self.root_cause_distribution(),
            "duplicate_distribution": self.duplicate_distribution()
        }


def analyze_defects(bugs):
    analytics = DefectPatternAnalytics(bugs)
    return analytics.get_summary()