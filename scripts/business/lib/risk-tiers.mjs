export const RISK_TIER_ORDER = [
  "tier_0_observe",
  "tier_1_recommend",
  "tier_2_draft",
  "tier_3_execute_reversible",
  "tier_4_execute_with_gate",
  "tier_5_restricted"
];

export const RISK_TIER_DETAILS = {
  tier_0_observe: {
    level: 0,
    label: "Observe only",
    requiresHumanApproval: false,
    allowsAutonomousExecution: false
  },
  tier_1_recommend: {
    level: 1,
    label: "Recommend only",
    requiresHumanApproval: false,
    allowsAutonomousExecution: false
  },
  tier_2_draft: {
    level: 2,
    label: "Draft with human approval",
    requiresHumanApproval: true,
    allowsAutonomousExecution: false
  },
  tier_3_execute_reversible: {
    level: 3,
    label: "Execute reversible low-risk actions",
    requiresHumanApproval: false,
    allowsAutonomousExecution: true
  },
  tier_4_execute_with_gate: {
    level: 4,
    label: "Execute with human gate for critical step",
    requiresHumanApproval: true,
    allowsAutonomousExecution: true
  },
  tier_5_restricted: {
    level: 5,
    label: "Restricted until assurance case exists",
    requiresHumanApproval: true,
    allowsAutonomousExecution: false
  }
};

export function getRiskTierLevel(riskTier) {
  return RISK_TIER_DETAILS[riskTier]?.level ?? -1;
}

export function isKnownRiskTier(riskTier) {
  return Boolean(RISK_TIER_DETAILS[riskTier]);
}

export function isHighRiskTier(riskTier) {
  return getRiskTierLevel(riskTier) >= 4;
}

export function requiresHumanApprovalByTier(riskTier) {
  return Boolean(RISK_TIER_DETAILS[riskTier]?.requiresHumanApproval);
}

export function validateRiskTierValue(riskTier, label = "risk tier") {
  if (!isKnownRiskTier(riskTier)) {
    throw new Error(`Unknown ${label}: ${riskTier}`);
  }
  return true;
}
