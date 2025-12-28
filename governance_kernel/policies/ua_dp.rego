package iluminara

allow if {
  input.region == "UA"
  input.framework == "UA_DP"
  input.data_type != "personal_data"
}
