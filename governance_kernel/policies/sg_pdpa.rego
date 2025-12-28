package iluminara

allow if {
  input.region == "SG"
  input.framework == "SG_PDPA"
  input.data_type != "personal_data"
}
