package iluminara

allow if {
  input.region == "IN"
  input.framework == "IN_DPDP"
  input.data_type != "sensitive_personal_data"
}
