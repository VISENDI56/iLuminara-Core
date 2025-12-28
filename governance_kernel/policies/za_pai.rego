package iluminara

allow if {
  input.region == "ZA"
  input.framework == "ZA_PAI"
  input.data_type != "special_category_data"
}
