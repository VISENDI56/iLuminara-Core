package iluminara

allow if {
  input.region == "KE"
  input.framework == "KENYA_DPA_2019"
  input.data_type != "sensitive_personal_data"
}
