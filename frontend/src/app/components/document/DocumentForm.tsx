import { useForm } from "react-hook-form";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import { Label } from "@/app/components/ui/label";
import type {
  DocumentType,
  Ecran,
  OfficeLicence,
  Ordinateur,
} from "@/app/types";
import type { DocumentCreatePayload } from "@/app/services/document";

interface OwnerLink {
  ordinateur_id?: number | null;
  ecran_id?: number | null;
  office_licence_id?: number | null;
}

interface Props {
  onSubmit: (data: DocumentCreatePayload) => void;
  isPending?: boolean;
  defaultValues?: Partial<DocumentCreatePayload>;
  /** Lock the linked equipment when the form is opened from a two-step flow */
  fixedOwner?: OwnerLink;
  /** Optional pickers for standalone use (from the Documents tab) */
  ordinateurs?: Ordinateur[];
  ecrans?: Ecran[];
  licences?: OfficeLicence[];
  submitLabel?: string;
}

const TYPE_OPTIONS: { value: DocumentType; label: string }[] = [
  { value: "devis", label: "Devis" },
  { value: "bon_de_commande", label: "Bon de commande" },
  { value: "facture", label: "Facture" },
];

export function DocumentForm({
  onSubmit,
  isPending,
  defaultValues,
  fixedOwner,
  ordinateurs,
  ecrans,
  licences,
  submitLabel = "Enregistrer le document",
}: Props) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<DocumentCreatePayload>({
    defaultValues: {
      type: defaultValues?.type ?? "facture",
      nom: defaultValues?.nom ?? "",
      numero: defaultValues?.numero ?? "",
      path: defaultValues?.path ?? "",
      date_document:
        defaultValues?.date_document ?? new Date().toISOString().split("T")[0],
      montant_ttc: defaultValues?.montant_ttc ?? null,
      montant_ht: defaultValues?.montant_ht ?? null,
      ordinateur_id:
        fixedOwner?.ordinateur_id ?? defaultValues?.ordinateur_id ?? null,
      ecran_id: fixedOwner?.ecran_id ?? defaultValues?.ecran_id ?? null,
      office_licence_id:
        fixedOwner?.office_licence_id ??
        defaultValues?.office_licence_id ??
        null,
    },
  });

  const type = watch("type");
  const isFacture = type === "facture";

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="type">Type *</Label>
        <select
          id="type"
          className="w-full border rounded-md px-3 py-2 text-sm"
          {...register("type", { required: true })}
        >
          {TYPE_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <Label htmlFor="numero">Numéro *</Label>
        <Input
          id="numero"
          placeholder="2024-0123"
          {...register("numero", { required: "Le numéro est obligatoire" })}
        />
        {errors.numero && (
          <p className="text-sm text-red-600 mt-1">{errors.numero.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="nom">Nom *</Label>
        <Input
          id="nom"
          placeholder="Facture Dell mars 2024"
          {...register("nom", { required: "Le nom est obligatoire" })}
        />
        {errors.nom && (
          <p className="text-sm text-red-600 mt-1">{errors.nom.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="path">Chemin réseau *</Label>
        <Input
          id="path"
          placeholder={"X:\\8-ADMINISTRATION GENERALE\\..."}
          {...register("path", { required: "Le chemin est obligatoire" })}
        />
        {errors.path && (
          <p className="text-sm text-red-600 mt-1">{errors.path.message}</p>
        )}
      </div>

      <div>
        <Label htmlFor="date_document">Date du document *</Label>
        <Input
          id="date_document"
          type="date"
          {...register("date_document", { required: "La date est obligatoire" })}
        />
      </div>

      {!fixedOwner && (
        <div className="grid grid-cols-3 gap-4">
          <div>
            <Label htmlFor="ordinateur_id">Ordinateur</Label>
            <select
              id="ordinateur_id"
              className="w-full border rounded-md px-3 py-2 text-sm"
              {...register("ordinateur_id", {
                setValueAs: (v) => (v === "" ? null : Number(v)),
              })}
            >
              <option value="">— Aucun —</option>
              {ordinateurs?.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.nom_reseau ?? o.tag ?? `#${o.id}`}
                </option>
              ))}
            </select>
          </div>
          <div>
            <Label htmlFor="ecran_id">Écran</Label>
            <select
              id="ecran_id"
              className="w-full border rounded-md px-3 py-2 text-sm"
              {...register("ecran_id", {
                setValueAs: (v) => (v === "" ? null : Number(v)),
              })}
            >
              <option value="">— Aucun —</option>
              {ecrans?.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.tag ?? `#${e.id}`}
                </option>
              ))}
            </select>
          </div>
          <div>
            <Label htmlFor="office_licence_id">Licence</Label>
            <select
              id="office_licence_id"
              className="w-full border rounded-md px-3 py-2 text-sm"
              {...register("office_licence_id", {
                setValueAs: (v) => (v === "" ? null : Number(v)),
              })}
            >
              <option value="">— Aucune —</option>
              {licences?.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.version ?? `#${l.id}`}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      {isFacture && (
        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label htmlFor="montant_ht">Montant HT</Label>
            <Input
              id="montant_ht"
              type="number"
              step="0.01"
              {...register("montant_ht", {
                setValueAs: (v) => (v === "" ? null : Number(v)),
              })}
            />
          </div>
          <div>
            <Label htmlFor="montant_ttc">Montant TTC</Label>
            <Input
              id="montant_ttc"
              type="number"
              step="0.01"
              {...register("montant_ttc", {
                setValueAs: (v) => (v === "" ? null : Number(v)),
              })}
            />
          </div>
        </div>
      )}

      <div className="flex justify-end pt-4">
        <Button type="submit" disabled={isPending}>
          {isPending ? "Enregistrement..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}
