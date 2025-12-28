package iluminara

allow if {
  input.region == "EU"
  input.framework == "EU_AI_ACT"
  input.data_type != "high_risk_ai_data"
}
