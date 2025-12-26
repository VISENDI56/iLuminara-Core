package iluminara

allow if {
  input.region == "CH"
  input.framework == "CH_FADP"
  input.data_type != "personal_data"
}
