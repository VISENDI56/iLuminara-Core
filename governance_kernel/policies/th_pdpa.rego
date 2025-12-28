package iluminara

allow if {
  input.region == "TH"
  input.framework == "TH_PDPA"
  input.data_type != "personal_data"
}
