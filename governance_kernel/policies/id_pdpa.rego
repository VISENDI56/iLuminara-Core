package iluminara

allow if {
  input.region == "ID"
  input.framework == "ID_PDPA"
  input.data_type != "personal_data"
}
