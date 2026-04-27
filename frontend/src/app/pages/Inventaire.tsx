// src/app/pages/Inventaire.tsx
import { useInventaire } from "@/app/hooks/useInventaire";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";

export function Inventaire() {
  const { data, isLoading, isError, error } = useInventaire();

  if (isLoading) {
    return <div className="p-6">Chargement...</div>;
  }

  if (isError) {
    return (
      <div className="p-6 text-red-600">
        Erreur : {error instanceof Error ? error.message : "inconnue"}
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Inventaire</h1>

      <Tabs defaultValue="ordinateurs">
        <TabsList>
          <TabsTrigger value="ordinateurs">
            Ordinateurs ({data.ordinateurs.length})
          </TabsTrigger>
          <TabsTrigger value="ecrans">
            Écrans ({data.ecrans.length})
          </TabsTrigger>
          <TabsTrigger value="licences">
            Licences ({data.licences.length})
          </TabsTrigger>
          <TabsTrigger value="devis">
            Devis ({data.devis.length})
          </TabsTrigger>
          <TabsTrigger value="bons_de_commande">
            Bons de commande ({data.bons_de_commande.length})
          </TabsTrigger>
          <TabsTrigger value="factures">
            Factures ({data.factures.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="ordinateurs" className="mt-6">
          <div>Tableau des ordinateurs (à venir)</div>
        </TabsContent>
        <TabsContent value="ecrans">
          <div>Tableau des écrans (à venir)</div>
        </TabsContent>
        <TabsContent value="licences">
          <div>Tableau des licences (à venir)</div>
        </TabsContent>
        <TabsContent value="devis">
          <div>Tableau des devis (à venir)</div>
        </TabsContent>
        <TabsContent value="bons_de_commande">
          <div>Tableau des bons de commande (à venir)</div>
        </TabsContent>
        <TabsContent value="factures">
          <div>Tableau des factures (à venir)</div>
        </TabsContent>
      </Tabs>
    </div>
  );
}