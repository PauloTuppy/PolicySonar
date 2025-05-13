import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"

const policySchema = z.object({
  policyName: z.string().min(1, "Policy name is required"),
  policyValue: z.number().min(0, "Value must be positive")
})

type PolicyFormValues = z.infer<typeof policySchema>

export function PolicyInput() {
  const form = useForm<PolicyFormValues>({
    resolver: zodResolver(policySchema),
    defaultValues: {
      policyName: "",
      policyValue: 0
    }
  })

  const onSubmit = (data: PolicyFormValues) => {
    console.log("Policy submitted:", data)
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Input
          placeholder="Policy name"
          {...form.register("policyName")}
        />
        {form.formState.errors.policyName && (
          <p className="text-sm text-destructive">
            {form.formState.errors.policyName.message}
          </p>
        )}
      </div>
      <div>
        <Input
          type="number"
          placeholder="Policy value"
          {...form.register("policyValue", { valueAsNumber: true })}
        />
        {form.formState.errors.policyValue && (
          <p className="text-sm text-destructive">
            {form.formState.errors.policyValue.message}
          </p>
        )}
      </div>
      <Button type="submit">Submit Policy</Button>
    </form>
  )
}
