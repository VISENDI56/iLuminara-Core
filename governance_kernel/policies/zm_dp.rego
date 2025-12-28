package iluminara

allow if {
  input.region == "ZM"
  input.framework == "ZM_DP"
  input.data_type != "personal_data"
}
