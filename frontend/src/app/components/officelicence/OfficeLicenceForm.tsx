import { useForm } from "react-hook-form";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import type { LicenceCreatePayload } from "@/app/services/officelicence";

interface Props {
  onSubmit: (data: LicenceCreatePayload) => void;
  isPending?: boolean;
  defaultValues?: Partial<LicenceCreatePayload>;
  submitLabel?: string;
}

export function OfficeLicenceForm({
  onSubmit,
  isPending,
  defaultValues,
  submitLabel = "Créer la licence",
}: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LicenceCreatePayload>({
    defaultValues: {
      version: defaultValues?.version ?? "",
      type_licence: defaultValues?.type_licence ?? "",
      date_achat:
        defaultValues?.date_achat ?? new Date().toISOString().split("T")[0],
      fournisseur: defaultValues?.fournisseur ?? "",
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="version">Version *</Label>
        <Input
          id="version"
          placeholder="Office 2021 Standard"
          {...register("version", { required: "La version est obligatoire" })}
        />
        {errors.version && (
          <p className="text-sm text-red-600 mt-1">{errors.version.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="type_licence">Type de licence</Label>
        <Input
          id="type_licence"
          placeholder="OEM"
          {...register("type_licence")}
        />
      </div>

      <div>
        <Label htmlFor="date_achat">Date d'achat</Label>
        <Input id="date_achat" type="date" {...register("date_achat")} />
      </div>

      <div>
        <Label htmlFor="fournisseur">Fournisseur</Label>
        <Input
          id="fournisseur"
          placeholder="Microsoft Direct"
          {...register("fournisseur")}
        />
      </div>

      <div className="flex justify-end pt-4">
        <Button type="submit" disabled={isPending}>
          {isPending ? "Enregistrement..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}
