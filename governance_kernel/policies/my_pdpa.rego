package iluminara

allow if {
  input.region == "MY"
  input.framework == "MY_PDPA"
  input.data_type != "personal_data"
}
