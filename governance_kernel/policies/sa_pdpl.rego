package iluminara

allow if {
  input.region == "SA"
  input.framework == "SA_PDPL"
  input.data_type != "personal_data"
}
