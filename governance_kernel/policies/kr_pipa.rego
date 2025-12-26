package iluminara

allow if {
  input.region == "KR"
  input.framework == "KR_PIPA"
  input.data_type != "personal_information"
}
