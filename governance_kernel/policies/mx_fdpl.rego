package iluminara

allow if {
  input.region == "MX"
  input.framework == "MX_FDPL"
  input.data_type != "personal_data"
}
