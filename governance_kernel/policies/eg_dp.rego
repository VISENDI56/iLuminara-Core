package iluminara

allow if {
  input.region == "EG"
  input.framework == "EG_DP"
  input.data_type != "personal_data"
}
