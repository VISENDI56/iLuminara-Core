package iluminara

allow if {
  input.region == "UG"
  input.framework == "UG_DP"
  input.data_type != "personal_data"
}
