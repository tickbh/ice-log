<template>
  <el-select
    v-model="selectedValue"
    :placeholder="placeholder"
    :disabled="disabled"
    clearable
    @change="handleChange"
  >
    <el-option
      v-for="option in options"
      :key="option.value"
      :label="option.label"
      :value="option.value"
    />
  </el-select>
</template>

<script setup lang="ts">
import DictAPI from "@/api/dict";
import LogsReadAPI from "@/api/logs_read";
import OptionsAPI from "@/api/options";

const props = defineProps({
  /**
   * 字典编码(eg: 性别-gender)
   */
  code: {
    type: String,
    default: "options",
  },
  rule: {
    type: String,
    required: true,
  },
  must: {
    type: Boolean,
    default: true,
  },
  modelValue: {
    type: [String, Number],
  },
  placeholder: {
    type: String,
    default: "请选择",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(["update:modelValue"]);

const options: Ref<OptionType[]> = ref([]);
const is_clear: Ref<Boolean> = ref(!props.must);

const selectedValue = ref<string | number | undefined>();

watch([options, () => props.modelValue], ([newOptions, newModelValue]) => {
  if (newOptions.length === 0) {
    // 下拉数据源加载未完成不回显
    return;
  }
  if (newModelValue == undefined) {
    selectedValue.value = undefined;
    return;
  }
  if (typeof newOptions[0].value === "number") {
    selectedValue.value = Number(newModelValue);
  } else if (typeof newOptions[0].value === "string") {
    selectedValue.value = String(newModelValue);
  } else {
    selectedValue.value = newModelValue;
  }
});

function handleChange(val?: string | number | undefined) {
  emits("update:modelValue", val);
}

function checkMust() {
  if (props.must && options.value.length > 0) {
    if (selectedValue.value == undefined) {
      handleChange(options.value[0].value);
    }
  }
}

onBeforeMount(() => {
  // 根据字典编码获取字典项
  // DictAPI.getOptions(props.code).then((data) => {
  //   options.value = data;
  // });
  if (props.rule == "logs_read") {
    OptionsAPI.getOptions(props.code, props.rule, () =>
      LogsReadAPI.options()
    ).then((data) => {
      options.value = data;
      checkMust();
    });
  } else {
    DictAPI.getOptions(props.code).then((data) => {
      options.value = data;
      checkMust();
    });
  }
});
</script>
