package iluminara

allow if {
  input.region == "PH"
  input.framework == "PH_DPA"
  input.data_type != "personal_data"
}
